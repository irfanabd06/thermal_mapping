
#include <stdio.h>
#include <string.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#include "driver/uart.h"
#include "driver/gpio.h"

#include "esp_err.h"

// ==========================================
// RS-485 CONFIGURATION
// ==========================================

#define RS485_UART UART_NUM_1

#define RS485_TX_GPIO GPIO_NUM_4
#define RS485_RX_GPIO GPIO_NUM_5
#define RS485_EN_GPIO GPIO_NUM_10

#define RS485_BAUD_RATE 9600

// Temporary test:
// Keep EN LOW throughout transmission.
#define RS485_EN_LEVEL 1

// ==========================================
// INITIALIZE RS-485
// ==========================================

static void rs485_init(void)
{
    // Configure UART
    uart_config_t uart_config = {
        .baud_rate = RS485_BAUD_RATE,
        .data_bits = UART_DATA_8_BITS,
        .parity = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
        .source_clk = UART_SCLK_DEFAULT
    };

    ESP_ERROR_CHECK(
        uart_driver_install(
            RS485_UART,
            1024,
            1024,
            0,
            NULL,
            0
        )
    );

    ESP_ERROR_CHECK(
        uart_param_config(
            RS485_UART,
            &uart_config
        )
    );

    ESP_ERROR_CHECK(
        uart_set_pin(
            RS485_UART,
            RS485_TX_GPIO,
            RS485_RX_GPIO,
            UART_PIN_NO_CHANGE,
            UART_PIN_NO_CHANGE
        )
    );

    // Configure EN as GPIO output
    ESP_ERROR_CHECK(
        gpio_reset_pin(RS485_EN_GPIO)
    );

    ESP_ERROR_CHECK(
        gpio_set_direction(
            RS485_EN_GPIO,
            GPIO_MODE_OUTPUT
        )
    );

    // Keep EN LOW for this test
    ESP_ERROR_CHECK(
        gpio_set_level(
            RS485_EN_GPIO,
            RS485_EN_LEVEL
        )
    );

    printf("RS485 UART initialized.\n");
    printf("Baud rate: %d\n", RS485_BAUD_RATE);
    printf("EN level: %d\n", RS485_EN_LEVEL);
}

// ==========================================
// MAIN APPLICATION
// ==========================================

void app_main(void)
{
    printf("\n");
    printf("============================\n");
    printf(" ESP32-C6 RS485 TEST\n");
    printf("============================\n");

    rs485_init();

    // Allow transceiver to settle
    vTaskDelay(pdMS_TO_TICKS(500));

    uint32_t message_count = 0;

    while (1)
    {
        message_count++;

        const char *message =
            "HELLO_FROM_ESP32\n";

        // EN remains LOW throughout the test.

        int written = uart_write_bytes(
            RS485_UART,
            message,
            strlen(message)
        );

        if (written < 0)
        {
            printf("RS485 UART write failed.\n");
        }
        else
        {
            esp_err_t status = uart_wait_tx_done(
                RS485_UART,
                pdMS_TO_TICKS(1000)
            );

            if (status == ESP_OK)
            {
                printf(
                    "RS485 TX attempt #%lu: %s",
                    (unsigned long)message_count,
                    message
                );
            }
            else
            {
                printf(
                    "RS485 TX timeout: %s\n",
                    esp_err_to_name(status)
                );
            }
        }

        // Send every 2 seconds
        vTaskDelay(pdMS_TO_TICKS(2000));
    }
}
