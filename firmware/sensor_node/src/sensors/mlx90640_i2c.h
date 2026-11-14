
#ifndef MLX90640_ESP_I2C_H
#define MLX90640_ESP_I2C_H

#include "esp_err.h"
#include "driver/i2c_master.h"

// Attach MLX90640 to an existing ESP-IDF I2C bus
esp_err_t mlx90640_attach_bus(
    i2c_master_bus_handle_t bus_handle
);

#endif
