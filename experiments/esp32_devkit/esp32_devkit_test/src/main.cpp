#include <Arduino.h>

void setup()
{
    Serial.begin(115200);

    Serial.println("CDE4301 Greenhouse Project");
    Serial.println("ESP32 DevKit test successful!");
}

void loop()
{
    Serial.println("ESP32 is running...");

    delay(1000);
}