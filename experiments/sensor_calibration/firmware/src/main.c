
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <math.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#include "driver/i2c_master.h"
#include "esp_err.h"
#include "esp_timer.h"

#include "config.h"
#include "sht45.h"
#include "mlx90640_i2c.h"
#include "MLX90640_API.h"

// ==========================================
// CONFIGURATION
// ==========================================

#define CAL_WIDTH 32
#define CAL_HEIGHT 24
#define CAL_PIXELS (CAL_WIDTH * CAL_HEIGHT)

#define LIVE_INTERVAL_MS 100
#define SHT45_INTERVAL_MS 1000

#define MAX_FRAME_ATTEMPTS MLX90640_MAX_ATTEMPTS

// ==========================================
// STATIC STORAGE
// ==========================================

static uint16_t mlx_eeprom[832];
static uint16_t mlx_frame[834];

static float mlx_temperatures[CAL_PIXELS];
static paramsMLX90640 mlx_params;

// ==========================================
// INITIALIZE I2C
// ==========================================

static i2c_master_bus_handle_t initialize_i2c(void)
{
    i2c_master_bus_config_t config = {
        .i2c_port = I2C_NUM_0,
        .sda_io_num = I2C_SDA_GPIO,
        .scl_io_num = I2C_SCL_GPIO,
        .clk_source = I2C_CLK_SRC_DEFAULT,
        .glitch_ignore_cnt = 7,
        .flags.enable_internal_pullup = true,
    };

    i2c_master_bus_handle_t bus = NULL;

    ESP_ERROR_CHECK(
        i2c_new_master_bus(&config, &bus)
    );

    return bus;
}

// ==========================================
// INITIALIZE MLX90640
// ==========================================

static bool initialize_mlx90640(
    i2c_master_bus_handle_t bus
)
{
    ESP_ERROR_CHECK(
        mlx90640_attach_bus(bus)
    );

    int status = MLX90640_DumpEE(
        MLX90640_I2C_ADDR,
        mlx_eeprom
    );

    if (status != 0)
    {
        printf("ERROR: EEPROM read failed: %d\n", status);
        return false;
    }

    status = MLX90640_ExtractParameters(
        mlx_eeprom,
        &mlx_params
    );

    if (status != 0)
    {
        printf("ERROR: Parameter extraction failed: %d\n", status);
        return false;
    }

    status = MLX90640_SetRefreshRate(
        MLX90640_I2C_ADDR,
        MLX90640_REFRESH_RATE
    );

    if (status != 0)
    {
        printf("ERROR: Refresh rate setup failed: %d\n", status);
        return false;
    }

    status = MLX90640_SetInterleavedMode(
        MLX90640_I2C_ADDR
    );

    if (status != 0)
    {
        printf("ERROR: Interleaved mode setup failed: %d\n", status);
        return false;
    }

    int mode = MLX90640_GetCurMode(
        MLX90640_I2C_ADDR
    );

    printf("MLX90640_MODE,%d\n", mode);

    if (mode != 0)
    {
        printf("ERROR: Expected interleaved mode\n");
        return false;
    }

    return true;
}

// ==========================================
// CAPTURE ONE COMPLETE THERMAL FRAME
// ==========================================

static bool capture_thermal_frame(void)
{
    bool received[2] = {false, false};
    int previous_subpage = -1;

    for (int attempt = 0;
         attempt < MAX_FRAME_ATTEMPTS;
         attempt++)
    {
        int status = MLX90640_GetFrameData(
            MLX90640_I2C_ADDR,
            mlx_frame
        );

        if (status < 0)
        {
            received[0] = false;
            received[1] = false;
            previous_subpage = -1;
            continue;
        }

        int subpage = mlx_frame[833];

        if (subpage != 0 && subpage != 1)
            continue;

        if (subpage == previous_subpage)
        {
            received[0] = false;
            received[1] = false;
        }

        previous_subpage = subpage;

        float ta = MLX90640_GetTa(
            mlx_frame,
            &mlx_params
        );

        // Preserve production calibration assumptions.
        float tr = ta - 8.0f;

        MLX90640_CalculateTo(
            mlx_frame,
            &mlx_params,
            MLX90640_EMISSIVITY,
            tr,
            mlx_temperatures
        );

        received[subpage] = true;

        if (received[0] && received[1])
        {
            MLX90640_BadPixelsCorrection(
                mlx_params.brokenPixels,
                mlx_temperatures,
                1,
                &mlx_params
            );

            MLX90640_BadPixelsCorrection(
                mlx_params.outlierPixels,
                mlx_temperatures,
                1,
                &mlx_params
            );

            return true;
        }
    }

    return false;
}

// ==========================================
// SEND SHT45 LIVE MEASUREMENT
// ==========================================

static void send_sht45_reading(void)
{
    sht45_data_t reading = {0};

    esp_err_t status = sht45_read(&reading);

    if (status == ESP_OK &&
        reading.valid &&
        isfinite(reading.temperature_c) &&
        isfinite(reading.humidity_rh))
    {
        printf(
            "SHT45,%.2f,%.2f\n",
            reading.temperature_c,
            reading.humidity_rh
        );
    }
    else
    {
        printf("SHT45_INVALID\n");
    }

    fflush(stdout);
}

// ==========================================
// SEND COMPLETE THERMAL FRAME
// ==========================================

static void send_live_frame(void)
{
    if (!capture_thermal_frame())
    {
        printf("FRAME_INVALID\n");
        fflush(stdout);
        return;
    }

    printf("FRAME_START\n");

    for (int row = 0; row < CAL_HEIGHT; row++)
    {
        for (int col = 0; col < CAL_WIDTH; col++)
        {
            int index = row * CAL_WIDTH + col;
            float t = mlx_temperatures[index];

            if (isfinite(t))
                printf("%.2f", t);
            else
                printf("nan");

            if (col < CAL_WIDTH - 1)
                printf(",");
        }

        printf("\n");
    }

    printf("FRAME_END\n");
    fflush(stdout);
}

// ==========================================
// MAIN APPLICATION
// ==========================================

void app_main(void)
{
    printf("\nSENSOR_CALIBRATION_BOOT\n");

    // Initialize I2C
    i2c_master_bus_handle_t bus =
        initialize_i2c();

    // Initialize SHT45
    ESP_ERROR_CHECK(
        sht45_init(bus)
    );

    printf("SHT45_READY\n");

    // Initialize MLX90640
    if (!initialize_mlx90640(bus))
    {
        printf("ERROR: MLX90640 initialization failed\n");
        return;
    }

    printf("MLX90640_READY\n");
    printf("LIVE_STREAM_STARTED\n");
    fflush(stdout);

    // Start with an immediate SHT45 reading.
    int64_t next_sht45_ms = 0;

    while (1)
    {
        int64_t now_ms =
            esp_timer_get_time() / 1000;

        // SHT45 approximately every second.
        if (now_ms >= next_sht45_ms)
        {
            send_sht45_reading();
            next_sht45_ms =
                esp_timer_get_time() / 1000
                + SHT45_INTERVAL_MS;
        }

        // Capture and transmit complete thermal frame.
        send_live_frame();

        vTaskDelay(
            pdMS_TO_TICKS(LIVE_INTERVAL_MS)
        );
    }
}
