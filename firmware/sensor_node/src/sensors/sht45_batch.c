
#include <stdlib.h>
#include <string.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#include "config.h"
#include "sensors/sht45.h"
#include "sensors/sht45_batch.h"

static int compare_float(const void *a, const void *b)
{
    float x = *(const float *)a;
    float y = *(const float *)b;

    return (x > y) - (x < y);
}

static float calculate_median(float *values, int count)
{
    qsort(
        values,
        count,
        sizeof(float),
        compare_float
    );

    if (count % 2 == 1)
        return values[count / 2];

    return (
        values[count / 2 - 1] +
        values[count / 2]
    ) / 2.0f;
}

bool sht45_read_batch(sht45_batch_data_t *result)
{
    if (result == NULL)
        return false;

    memset(result, 0, sizeof(*result));

    float temperatures[SHT45_SAMPLE_COUNT];
    float humidities[SHT45_SAMPLE_COUNT];

    int valid_count = 0;

    for (int i = 0; i < SHT45_SAMPLE_COUNT; i++)
    {
        sht45_data_t reading = {0};

        if (sht45_read(&reading) == ESP_OK &&
            reading.valid)
        {
            temperatures[valid_count] =
                reading.temperature_c;

            humidities[valid_count] =
                reading.humidity_rh;

            valid_count++;
        }

        // Space readings 1 second apart.
        // No unnecessary delay after last sample.
        if (i < SHT45_SAMPLE_COUNT - 1)
        {
            vTaskDelay(
                pdMS_TO_TICKS(
                    SHT45_SAMPLE_SPACING_MS
                )
            );
        }
    }

    result->valid_samples = valid_count;

    if (valid_count == 0)
        return false;

    result->temperature_median_c =
        calculate_median(temperatures, valid_count);

    result->humidity_median_rh =
        calculate_median(humidities, valid_count);

    result->valid = true;

    return true;
}
