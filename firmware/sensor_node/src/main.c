
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#include "driver/i2c_master.h"
#include "esp_err.h"
#include "esp_timer.h"

#include "config.h"
#include "telemetry.h"

#include "sensors/sht45.h"
#include "sensors/sht45_batch.h"
#include "sensors/mlx90640_i2c.h"

#include "MLX90640_API.h"

#include "communication/rs485.h"

// ==========================================
// STATIC STORAGE
// ==========================================

static uint16_t mlx_eeprom[832];
static uint16_t mlx_frame[834];

static float mlx_temperatures[THERMAL_PIXELS];
static float mlx_pixel_sum[THERMAL_PIXELS];

static paramsMLX90640 mlx_params;
static telemetry_data_t telemetry;

// ==========================================
// CAPTURE ONE COMPLETE MLX90640 FRAME
// ==========================================

static bool capture_thermal_frame(void)
{
    bool received[2] = {false, false};
    int previous_subpage = -1;

    for (int attempt = 0;
         attempt < MLX90640_MAX_ATTEMPTS;
         attempt++)
    {
        int status = MLX90640_GetFrameData(
            MLX90640_I2C_ADDR,
            mlx_frame
        );

        if (status < 0)
        {
            printf(
                "ERROR: MLX90640 read failed: %d\n",
                status
            );

            received[0] = false;
            received[1] = false;
            previous_subpage = -1;
            continue;
        }

        int subpage = mlx_frame[833];

        if (subpage != 0 && subpage != 1)
        {
            printf(
                "ERROR: Invalid subpage %d\n",
                subpage
            );
            continue;
        }

        // Restart pairing if the same
        // subpage is received consecutively.
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

        // Provisional reflected-temperature
        // assumption. Revalidate on site.
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
// AVERAGE MULTIPLE THERMAL FRAMES
// ==========================================

static uint8_t mlx90640_average_frames(void)
{
    memset(
        mlx_pixel_sum,
        0,
        sizeof(mlx_pixel_sum)
    );

    uint8_t valid_frames = 0;

    printf(
        "MLX90640: Starting %d-frame acquisition\n",
        MLX90640_FRAME_COUNT
    );

    for (int frame = 0;
         frame < MLX90640_FRAME_COUNT;
         frame++)
    {
        if (!capture_thermal_frame())
        {
            printf(
                "WARNING: Thermal frame %d failed\n",
                frame + 1
            );
            continue;
        }

        for (int pixel = 0;
             pixel < THERMAL_PIXELS;
             pixel++)
        {
            mlx_pixel_sum[pixel] +=
                mlx_temperatures[pixel];
        }

        valid_frames++;
    }

    // Require all requested frames
    // for the initial validation.
    if (valid_frames != MLX90640_FRAME_COUNT)
    {
        printf(
            "WARNING: Incomplete thermal batch %u/%d\n",
            (unsigned int)valid_frames,
            MLX90640_FRAME_COUNT
        );

        return valid_frames;
    }

    for (int pixel = 0;
         pixel < THERMAL_PIXELS;
         pixel++)
    {
        telemetry.thermal_pixels[pixel] =
            mlx_pixel_sum[pixel] / valid_frames;
    }

    printf(
        "MLX90640: Averaged %u frames\n",
        (unsigned int)valid_frames
    );

    return valid_frames;
}

// ==========================================
// INITIALIZE I2C
// ==========================================

static i2c_master_bus_handle_t initialize_i2c(void)
{
    i2c_master_bus_config_t bus_config = {
        .i2c_port = I2C_NUM_0,
        .sda_io_num = I2C_SDA_GPIO,
        .scl_io_num = I2C_SCL_GPIO,
        .clk_source = I2C_CLK_SRC_DEFAULT,
        .glitch_ignore_cnt = 7,
        .flags.enable_internal_pullup = true,
    };

    i2c_master_bus_handle_t bus_handle = NULL;

    ESP_ERROR_CHECK(
        i2c_new_master_bus(
            &bus_config,
            &bus_handle
        )
    );

    return bus_handle;
}

// ==========================================
// INITIALIZE MLX90640
// ==========================================

static bool initialize_mlx90640(
    i2c_master_bus_handle_t bus_handle
)
{
    ESP_ERROR_CHECK(
        mlx90640_attach_bus(bus_handle)
    );

    int status = MLX90640_DumpEE(
        MLX90640_I2C_ADDR,
        mlx_eeprom
    );

    if (status != 0)
    {
        printf(
            "ERROR: EEPROM read failed: %d\n",
            status
        );
        return false;
    }

    status = MLX90640_ExtractParameters(
        mlx_eeprom,
        &mlx_params
    );

    if (status != 0)
    {
        printf(
            "ERROR: Calibration extraction failed: %d\n",
            status
        );
        return false;
    }

    status = MLX90640_SetRefreshRate(
        MLX90640_I2C_ADDR,
        MLX90640_REFRESH_RATE
    );

    if (status != 0)
    {
        printf(
            "ERROR: Refresh rate configuration failed\n"
        );
        return false;
    }

    status = MLX90640_SetInterleavedMode(
        MLX90640_I2C_ADDR
    );

    if (status != 0)
    {
        printf(
            "ERROR: Interleaved mode configuration failed\n"
        );
        return false;
    }

    int mode = MLX90640_GetCurMode(
        MLX90640_I2C_ADDR
    );

    printf("MLX90640 mode: %d\n", mode);

    if (mode != 0)
    {
        printf(
            "ERROR: Expected interleaved mode (0)\n"
        );
        return false;
    }

    return true;
}

// ==========================================
// MAIN APPLICATION
// ==========================================

void app_main(void)
{
    printf("\n====================================\n");
    printf(" GREENHOUSE SENSOR NODE\n");
    printf(" ESP32-C6 | SHT45 | MLX90640-BAB\n");
    printf("====================================\n");

    // 1. Initialize I2C
    i2c_master_bus_handle_t bus_handle =
        initialize_i2c();

    printf("I2C initialized.\n");

    // 2. Initialize SHT45
    ESP_ERROR_CHECK(
        sht45_init(bus_handle)
    );

    printf("SHT45 initialized.\n");

    // 3. Initialize MLX90640
    if (!initialize_mlx90640(bus_handle))
    {
        printf("MLX90640 initialization failed\n");
        return;
    }

    printf("MLX90640 initialized.\n");

    // Initialize RS-485 communication
    ESP_ERROR_CHECK(rs485_init());

    printf("RS485 initialized.\n");

    // 4. Initialize telemetry
    memset(&telemetry, 0, sizeof(telemetry));

    telemetry.node_id = NODE_ID;
    telemetry.sequence = 0;

    printf("\nSENSORS_READY\n");

    // ======================================
    // MAIN MEASUREMENT LOOP
    // ======================================

    while (1)
    {
        // ----------------------------------
        // A. Start measurement cycle
        // ----------------------------------

        int64_t cycle_start_us =
            esp_timer_get_time();

        telemetry.measurement_started_ms =
            (uint64_t)(cycle_start_us / 1000);

        telemetry.sht45_valid = false;
        telemetry.mlx90640_valid = false;

        telemetry.sht45_valid_samples = 0;
        telemetry.mlx90640_valid_frames = 0;

        printf("\n====================================\n");
        printf(" STARTING MEASUREMENT CYCLE\n");
        printf("====================================\n");

        // ----------------------------------
        // B. SHT45 batch measurement
        // ----------------------------------

        int64_t sht_start_us =
            esp_timer_get_time();

        sht45_batch_data_t air_batch = {0};

        bool sht_success =
            sht45_read_batch(&air_batch);

        telemetry.sht45_duration_ms =
            (uint32_t)(
                (esp_timer_get_time() -
                 sht_start_us) / 1000
            );

        telemetry.sht45_valid_samples =
            air_batch.valid_samples;

        if (sht_success &&
            air_batch.valid &&
            air_batch.valid_samples >=
                SHT45_MIN_VALID_SAMPLES)
        {
            telemetry.air_temperature_c =
                air_batch.temperature_median_c;

            telemetry.humidity_rh =
                air_batch.humidity_median_rh;

            telemetry.sht45_valid = true;
        }

        printf(
            "SHT45: %u/%d samples | %lu ms\n",
            (unsigned int)
                telemetry.sht45_valid_samples,
            SHT45_SAMPLE_COUNT,
            (unsigned long)
                telemetry.sht45_duration_ms
        );

        // ----------------------------------
        // C. MLX90640 batch measurement
        // ----------------------------------

        int64_t mlx_start_us =
            esp_timer_get_time();

        uint8_t valid_frames =
            mlx90640_average_frames();

        telemetry.mlx90640_duration_ms =
            (uint32_t)(
                (esp_timer_get_time() -
                 mlx_start_us) / 1000
            );

        telemetry.mlx90640_valid_frames =
            valid_frames;

        telemetry.mlx90640_valid =
            (valid_frames == MLX90640_FRAME_COUNT);

        printf(
            "MLX90640: %u/%d frames | %lu ms\n",
            (unsigned int)valid_frames,
            MLX90640_FRAME_COUNT,
            (unsigned long)
                telemetry.mlx90640_duration_ms
        );

        // ----------------------------------
        // D. Finish measurement
        // ----------------------------------

        telemetry.measurement_completed_ms =
            (uint64_t)(
                esp_timer_get_time() / 1000
            );

        telemetry.sequence++;

        telemetry.uptime_ms =
            telemetry.measurement_completed_ms;

        // ----------------------------------
        // E. JSON telemetry transmission
        // ----------------------------------

        printf("\nTELEMETRY_START\n");

        int64_t tx_start_us =
            esp_timer_get_time();

        telemetry_send_json(&telemetry);

        fflush(stdout);

        uint32_t tx_duration_ms =
            (uint32_t)(
                (esp_timer_get_time() -
                 tx_start_us) / 1000
            );

        printf("TELEMETRY_END\n");

        printf(
            "Telemetry serialization/output: %lu ms\n",
            (unsigned long)tx_duration_ms
        );

        // ----------------------------------
        // F. Wait until next cycle
        // ----------------------------------

        int64_t elapsed_ms =
            (esp_timer_get_time() -
             cycle_start_us) / 1000;

        if (elapsed_ms < TEST_INTERVAL_MS)
        {
            vTaskDelay(
                pdMS_TO_TICKS(
                    TEST_INTERVAL_MS - elapsed_ms
                )
            );
        }
    }
}
