
#ifndef SHT45_H
#define SHT45_H

#include <stdbool.h>
#include <stdint.h>

#include "esp_err.h"
#include "driver/i2c_master.h"

// SHT45 I2C configuration
#define SHT45_I2C_ADDRESS  0x44
#define SHT45_I2C_FREQ_HZ  100000

// Sensor measurement structure
typedef struct {
    float temperature_c;
    float humidity_rh;
    bool valid;
} sht45_data_t;

// Initialize SHT45 on an existing I2C bus
esp_err_t sht45_init(i2c_master_bus_handle_t bus_handle);

// Read temperature and relative humidity
esp_err_t sht45_read(sht45_data_t *data);

#endif // SHT45_H
