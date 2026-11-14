
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <inttypes.h>

#include "telemetry.h"
#include "communication/rs485.h"

// Buffer large enough for 768 thermal pixels.
// Static storage avoids large stack allocations.
#define TELEMETRY_JSON_BUFFER_SIZE 16384

static char json_buffer[TELEMETRY_JSON_BUFFER_SIZE];

void telemetry_send_json(const telemetry_data_t *data)
{
    if (data == NULL)
        return;

    size_t offset = 0;
    int written;

    // Helper macro: append formatted text safely.
    // Abort if the buffer is too small.
    #define APPEND_JSON(...) do {                          \
        if (offset >= sizeof(json_buffer)) return;        \
        written = snprintf(                               \
            json_buffer + offset,                          \
            sizeof(json_buffer) - offset,                  \
            __VA_ARGS__                                    \
        );                                                \
        if (written < 0 ||                                \
            (size_t)written >= sizeof(json_buffer) - offset) { \
            printf("ERROR: JSON buffer overflow\n");     \
            return;                                       \
        }                                                 \
        offset += (size_t)written;                         \
    } while (0)

    // ==================================
    // Metadata and timing
    // ==================================

    APPEND_JSON("{");

    APPEND_JSON(
        "\"node_id\":%u,",
        (unsigned int)data->node_id
    );

    APPEND_JSON(
        "\"sequence\":%" PRIu32 ",",
        data->sequence
    );

    APPEND_JSON(
        "\"uptime_ms\":%" PRIu64 ",",
        data->uptime_ms
    );

    APPEND_JSON(
        "\"measurement_started_ms\":%" PRIu64 ",",
        data->measurement_started_ms
    );

    APPEND_JSON(
        "\"measurement_completed_ms\":%" PRIu64 ",",
        data->measurement_completed_ms
    );

    APPEND_JSON(
        "\"timing\":{"
        "\"sht45_duration_ms\":%" PRIu32 ","
        "\"mlx90640_duration_ms\":%" PRIu32
        "},",
        data->sht45_duration_ms,
        data->mlx90640_duration_ms
    );

    APPEND_JSON(
        "\"sampling\":{"
        "\"sht45_valid_samples\":%u,"
        "\"mlx90640_valid_frames\":%u"
        "},",
        (unsigned int)data->sht45_valid_samples,
        (unsigned int)data->mlx90640_valid_frames
    );

    // ==================================
    // SHT45
    // ==================================

    APPEND_JSON("\"sht45\":{");

    if (data->sht45_valid &&
        isfinite(data->air_temperature_c) &&
        isfinite(data->humidity_rh))
    {
        APPEND_JSON(
            "\"temperature_c\":%.2f,",
            data->air_temperature_c
        );

        APPEND_JSON(
            "\"humidity_rh\":%.2f,",
            data->humidity_rh
        );

        APPEND_JSON("\"valid\":true");
    }
    else
    {
        APPEND_JSON(
            "\"temperature_c\":null,"
            "\"humidity_rh\":null,"
            "\"valid\":false"
        );
    }

    APPEND_JSON("},");

    // ==================================
    // MLX90640
    // ==================================

    APPEND_JSON("\"mlx90640\":{");

    APPEND_JSON(
        "\"width\":%d,"
        "\"height\":%d,"
        "\"emissivity\":0.95,",
        THERMAL_WIDTH,
        THERMAL_HEIGHT
    );

    APPEND_JSON(
        "\"valid\":%s,",
        data->mlx90640_valid ? "true" : "false"
    );

    APPEND_JSON("\"pixels_c\":[");

    if (data->mlx90640_valid)
    {
        for (int i = 0; i < THERMAL_PIXELS; i++)
        {
            float t = data->thermal_pixels[i];

            if (isfinite(t))
            {
                APPEND_JSON("%.2f", t);
            }
            else
            {
                APPEND_JSON("null");
            }

            if (i < THERMAL_PIXELS - 1)
            {
                APPEND_JSON(",");
            }
        }
    }

    APPEND_JSON("]}");
    APPEND_JSON("}\n");

    #undef APPEND_JSON

    // ==================================
    // USB SERIAL DEBUG OUTPUT
    // ==================================

    printf("%s", json_buffer);
    fflush(stdout);

    // ==================================
    // RS-485 TRANSMISSION
    // ==================================

    esp_err_t status = rs485_send(
        json_buffer,
        offset
    );

    if (status == ESP_OK)
    {
        printf(
            "RS485: JSON transmitted (%u bytes)\n",
            (unsigned int)offset
        );
    }
    else
    {
        printf(
            "RS485: Transmission failed: %s\n",
            esp_err_to_name(status)
        );
    }
}
