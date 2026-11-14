
idf_component_register(
    SRCS
        "main.c"
        "telemetry.c"
        "communication/rs485.c"
        "sensors/sht45.c"
        "sensors/sht45_batch.c"
        "sensors/mlx90640_i2c.c"
        "../lib/mlx90640-library/functions/MLX90640_API.c"

    INCLUDE_DIRS
        "."
        "../include"
        "../lib/mlx90640-library/headers"

    REQUIRES
        esp_driver_i2c
        esp_driver_uart
        esp_driver_gpio
        esp_timer
)
