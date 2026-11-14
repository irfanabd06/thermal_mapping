
#include "mlx90640_i2c.h"
#include "MLX90640_I2C_Driver.h"

#include <stdint.h>
#include <stdlib.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#define MLX90640_ADDRESS 0x33
#define MLX90640_TIMEOUT_MS 1000

static i2c_master_bus_handle_t s_bus = NULL;
static i2c_master_dev_handle_t s_device = NULL;

// Register the shared I2C bus
esp_err_t mlx90640_attach_bus(
    i2c_master_bus_handle_t bus_handle)
{
    if (bus_handle == NULL) {
        return ESP_ERR_INVALID_ARG;
    }

    if (s_device != NULL) {
        return ESP_ERR_INVALID_STATE;
    }

    i2c_device_config_t dev_config = {
        .dev_addr_length = I2C_ADDR_BIT_LEN_7,
        .device_address = MLX90640_ADDRESS,
        .scl_speed_hz = 100000,
    };

    esp_err_t err = i2c_master_bus_add_device(
        bus_handle, &dev_config, &s_device
    );

    if (err == ESP_OK) {
        s_bus = bus_handle;
    }

    return err;
}

// Melexis compatibility functions
void MLX90640_I2CInit(void)
{
    // Bus is initialized by main.c
}

void MLX90640_I2CFreqSet(int freq)
{
    // Frequency configured in attach_bus().
    // This adapter currently uses 400 kHz.
    (void)freq;
}

int MLX90640_I2CGeneralReset(void)
{
    // Not implemented: do not issue a general-call
    // reset because SHT45 shares the same bus.
    return -1;
}

int MLX90640_I2CRead(
    uint8_t slaveAddr,
    uint16_t startAddress,
    uint16_t nMemAddressRead,
    uint16_t *data)
{
    if (s_device == NULL ||
        slaveAddr != MLX90640_ADDRESS ||
        data == NULL ||
        nMemAddressRead == 0) {
        return -1;
    }

    // Each MLX90640 register is 16 bits.
    size_t bytes = (size_t)nMemAddressRead * 2;

    uint8_t *buffer = malloc(bytes);

    if (buffer == NULL) {
        return -1;
    }

    uint8_t reg[2] = {
        (uint8_t)(startAddress >> 8),
        (uint8_t)(startAddress & 0xFF)
    };

    esp_err_t err = i2c_master_transmit_receive(
        s_device,
        reg, sizeof(reg),
        buffer, bytes,
        MLX90640_TIMEOUT_MS
    );

    if (err == ESP_OK) {
        for (uint16_t i = 0; i < nMemAddressRead; i++) {
            data[i] =
                ((uint16_t)buffer[2 * i] << 8) |
                buffer[2 * i + 1];
        }
    }

    free(buffer);

    return (err == ESP_OK) ? 0 : -1;
}

int MLX90640_I2CWrite(
    uint8_t slaveAddr,
    uint16_t writeAddress,
    uint16_t data)
{
    if (s_device == NULL ||
        slaveAddr != MLX90640_ADDRESS) {
        return -1;
    }

    uint8_t buffer[4] = {
        (uint8_t)(writeAddress >> 8),
        (uint8_t)(writeAddress & 0xFF),
        (uint8_t)(data >> 8),
        (uint8_t)(data & 0xFF)
    };

    esp_err_t err = i2c_master_transmit(
        s_device,
        buffer, sizeof(buffer),
        MLX90640_TIMEOUT_MS
    );

    return (err == ESP_OK) ? 0 : -1;
}
