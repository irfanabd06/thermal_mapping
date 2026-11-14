
#ifndef RS485_H
#define RS485_H

#include <stddef.h>
#include "esp_err.h"

esp_err_t rs485_init(void);

esp_err_t rs485_send(
    const char *data,
    size_t length
);

#endif
