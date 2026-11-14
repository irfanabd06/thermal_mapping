
#ifndef CONFIG_H
#define CONFIG_H

// ==========================================
// GREENHOUSE SENSOR NODE CONFIGURATION
// ==========================================

// ------------------------------------------
// 1. Node identification
// ------------------------------------------

#define NODE_ID 1

// ------------------------------------------
// 2. I2C configuration
// ------------------------------------------

// IMPORTANT:
// Replace these with your existing working
// SDA and SCL GPIO assignments if different.

#define I2C_SDA_GPIO 6
#define I2C_SCL_GPIO 7

// ------------------------------------------
// 3. Operating modes
// ------------------------------------------

#define MODE_MONITORING      0
#define MODE_ACTIVE_CONTROL 1

#define DEFAULT_OPERATING_MODE MODE_MONITORING

// ------------------------------------------
// 4. Measurement intervals
// ------------------------------------------

// Monitoring: every 30 minutes
#define MONITORING_INTERVAL_MS 1800000UL

// Active control: every 5 minutes
#define ACTIVE_INTERVAL_MS 300000UL

// Development communication test: 1 minute
#define TEST_INTERVAL_MS 60000UL

// ------------------------------------------
// 5. SHT45 configuration
// ------------------------------------------

// Collect 10 measurements per cycle
#define SHT45_SAMPLE_COUNT 10

// Time between measurements: 1 second
#define SHT45_SAMPLE_SPACING_MS 1000UL

// Minimum successful readings required
#define SHT45_MIN_VALID_SAMPLES 8

// ------------------------------------------
// 6. MLX90640 configuration
// ------------------------------------------

// Average 10 complete thermal frames
#define MLX90640_FRAME_COUNT 10

// MLX90640 refresh rate: 2 Hz
#define MLX90640_REFRESH_RATE 0x02

// Surface emissivity
#define MLX90640_EMISSIVITY 0.95f

// Maximum subpage acquisition attempts
#define MLX90640_MAX_ATTEMPTS 10

// Sensor I2C address
#define MLX90640_I2C_ADDR 0x33

// Thermal sensor resolution
#define MLX90640_WIDTH 32
#define MLX90640_HEIGHT 24
#define MLX90640_PIXELS 768

// ------------------------------------------
// 7. Communication configuration
// ------------------------------------------

#define SERIAL_BAUD_RATE 115200

// ------------------------------------------
// 8. Power management
// ------------------------------------------

// 0 = Normal operation during development
// 1 = Deep sleep (to be implemented later)
#define ENABLE_DEEP_SLEEP 0

#endif // CONFIG_H