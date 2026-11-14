#ifndef SENSOR_DATA_H
#define SENSOR_DATA_H

#include <stdint.h>
#include <stdbool.h>

typedef struct {
    uint16_t node_id;
    uint32_t timestamp_ms;

    float temperature_c;
    float humidity_rh;

    bool valid;
} sensor_data_t;

#endif