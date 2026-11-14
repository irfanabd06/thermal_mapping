
#include "sht45.h"

#include <stddef.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

// SHT45 high-precision measurement command
#define SHT45_MEASURE_CMD  0xFD

// I2C timeout in milliseconds
#define SHT45_TIMEOUT_MS   100

// SHT45 device handle
static i2c_master_dev_handle_t sht45_handle = NULL;


// CRC-8 validation
// Polynomial: 0x31
// Initial value: 0xFF
static uint8_t sht45_crc8(const uint8_t *data, size_t len)
{
    uint8_t crc = 0xFF;

    for (size_t i = 0; i < len; i++)
    {
        crc ^= data[i];

        for (int bit = 0; bit < 8; bit++)
        {
            if (crc & 0x80)
            {
                crc = (crc << 1) ^ 0x31;
            }
            else
            {
                crc <<= 1;
            }
        }
    }

    return crc;
}


// Initialize SHT45
esp_err_t sht45_init(i2c_master_bus_handle_t bus_handle)
{
    if (bus_handle == NULL)
    {
        return ESP_ERR_INVALID_ARG;
    }

    if (sht45_handle != NULL)
    {
        return ESP_ERR_INVALID_STATE;
    }

    i2c_device_config_t dev_config = {
        .dev_addr_length = I2C_ADDR_BIT_LEN_7,
        .device_address = SHT45_I2C_ADDRESS,
        .scl_speed_hz = SHT45_I2C_FREQ_HZ,
    };

    return i2c_master_bus_add_device(
        bus_handle,
        &dev_config,
        &sht45_handle
    );
}


// Read temperature and humidity
esp_err_t sht45_read(sht45_data_t *data)
{
    if (data == NULL)
    {
        return ESP_ERR_INVALID_ARG;
    }

    data->valid = false;

    if (sht45_handle == NULL)
    {
        return ESP_ERR_INVALID_STATE;
    }

    uint8_t command = SHT45_MEASURE_CMD;
    uint8_t raw_data[6];

    // Step 1: Trigger measurement
    esp_err_t err = i2c_master_transmit(
        sht45_handle,
        &command,
        1,
        SHT45_TIMEOUT_MS
    );

    if (err != ESP_OK)
    {
        return err;
    }

    // Step 2: Wait for measurement completion
    vTaskDelay(pdMS_TO_TICKS(20));

    // Step 3: Read six bytes
    err = i2c_master_receive(
        sht45_handle,
        raw_data,
        sizeof(raw_data),
        SHT45_TIMEOUT_MS
    );

    if (err != ESP_OK)
    {
        return err;
    }

    // Step 4: Validate temperature CRC
    if (sht45_crc8(raw_data, 2) != raw_data[2])
    {
        return ESP_ERR_INVALID_CRC;
    }

    // Step 5: Validate humidity CRC
    if (sht45_crc8(&raw_data[3], 2) != raw_data[5])
    {
        return ESP_ERR_INVALID_CRC;
    }

    // Step 6: Combine raw bytes
    uint16_t raw_temp =
        ((uint16_t)raw_data[0] << 8) | raw_data[1];

    uint16_t raw_rh =
        ((uint16_t)raw_data[3] << 8) | raw_data[4];

    // Step 7: Convert to physical measurements
    data->temperature_c =
        -45.0f + 175.0f * raw_temp / 65535.0f;

    data->humidity_rh =
        -6.0f + 125.0f * raw_rh / 65535.0f;

    // Limit humidity to physical range
    if (data->humidity_rh < 0.0f)
    {
        data->humidity_rh = 0.0f;
    }

    if (data->humidity_rh > 100.0f)
    {
        data->humidity_rh = 100.0f;
    }

    // Measurement successfully validated
    data->valid = true;

    return ESP_OK;
}
