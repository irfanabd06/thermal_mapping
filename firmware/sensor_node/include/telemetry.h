
#ifndef TELEMETRY_H
#define TELEMETRY_H

#include <stdint.h>
#include <stdbool.h>

#define THERMAL_WIDTH 32
#define THERMAL_HEIGHT 24
#define THERMAL_PIXELS 768

typedef struct
{
    // Node identification
    uint16_t node_id;
    uint32_t sequence;
    uint64_t uptime_ms;

    // Measurement timestamps
    uint64_t measurement_started_ms;
    uint64_t measurement_completed_ms;

    // Sensor acquisition durations
    uint32_t sht45_duration_ms;
    uint32_t mlx90640_duration_ms;

    // Successful sample counts
    uint8_t sht45_valid_samples;
    uint8_t mlx90640_valid_frames;

    // SHT45 measurements
    float air_temperature_c;
    float humidity_rh;
    bool sht45_valid;

    // MLX90640 measurements
    float thermal_pixels[THERMAL_PIXELS];
    bool mlx90640_valid;

} telemetry_data_t;

// JSON serialization
void telemetry_send_json(
    const telemetry_data_t *data
);

#endif
