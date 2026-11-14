#pragma once

#include <stdint.h>
#include <stdbool.h>

typedef struct {
    float temperature_median_c;
    float humidity_median_rh;
    uint8_t valid_samples;
    bool valid;
} sht45_batch_data_t;

bool sht45_read_batch(sht45_batch_data_t *result);