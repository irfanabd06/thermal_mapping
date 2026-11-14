
#include <stdint.h>

#include "communication/rs485.h"

#include "driver/uart.h"
#include "driver/gpio.h"

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#define RS485_UART UART_NUM_1

#define RS485_TX_GPIO GPIO_NUM_4
#define RS485_RX_GPIO GPIO_NUM_5
#define RS485_EN_GPIO GPIO_NUM_10

#define RS485_BAUD_RATE 9600

esp_err_t rs485_init(void)
{
    uart_config_t config = {
        .baud_rate = RS485_BAUD_RATE,
        .data_bits = UART_DATA_8_BITS,
        .parity = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
        .source_clk = UART_SCLK_DEFAULT
    };

    esp_err_t err = uart_driver_install(
        RS485_UART, 1024, 1024, 0, NULL, 0
    );
    if (err != ESP_OK) return err;

    err = uart_param_config(RS485_UART, &config);
    if (err != ESP_OK) return err;

    err = uart_set_pin(
        RS485_UART,
        RS485_TX_GPIO,
        RS485_RX_GPIO,
        UART_PIN_NO_CHANGE,
        UART_PIN_NO_CHANGE
    );
    if (err != ESP_OK) return err;

    err = gpio_reset_pin(RS485_EN_GPIO);
    if (err != ESP_OK) return err;

    err = gpio_set_direction(
        RS485_EN_GPIO,
        GPIO_MODE_OUTPUT
    );
    if (err != ESP_OK) return err;

    // Bench-tested configuration:
    // HIGH enables transmission.
    return gpio_set_level(RS485_EN_GPIO, 1);
}

esp_err_t rs485_send(
    const char *data,
    size_t length
)
{
    if (data == NULL || length == 0)
        return ESP_ERR_INVALID_ARG;

    int written = uart_write_bytes(
        RS485_UART,
        data,
        length
    );

    if (written < 0 || (size_t)written != length)
        return ESP_FAIL;

    return uart_wait_tx_done(
        RS485_UART,
        pdMS_TO_TICKS(15000)
    );
}
