
# ==========================================
# CDE4301 Sensor Calibration
# ESP32-C6 | SHT45 | MLX90640
# ==========================================

# Reference existing sensor_node firmware
# without modifying the original files.

get_filename_component(
    SENSOR_NODE
    "${CMAKE_CURRENT_LIST_DIR}/../../../../firmware/sensor_node"
    ABSOLUTE
)

idf_component_register(
    SRCS
        "main.c"
        "${SENSOR_NODE}/src/sensors/sht45.c"
        "${SENSOR_NODE}/src/sensors/mlx90640_i2c.c"
        "${SENSOR_NODE}/lib/mlx90640-library/functions/MLX90640_API.c"

    INCLUDE_DIRS
        "."
        "${SENSOR_NODE}/include"
        "${SENSOR_NODE}/include/sensors"
        "${SENSOR_NODE}/src/sensors"
        "${SENSOR_NODE}/lib/mlx90640-library/headers"

    REQUIRES
        esp_driver_i2c
        esp_driver_uart
        esp_timer
)

message(
    STATUS
    "Sensor node directory: ${SENSOR_NODE}"
)
