#include <Arduino.h>

const int MCP9700_PIN = 34;

void setup()
{
    Serial.begin(115200);
    delay(1000);

    Serial.println("CDE4301 - MCP9700 Test");
    Serial.println("----------------------");
}

void loop()
{
    const int NUM_SAMPLES = 20;

    long adcSum = 0;
    long voltageSum = 0;

    for (int i = 0; i < NUM_SAMPLES; i++)
    {
        adcSum += analogRead(MCP9700_PIN);
        voltageSum += analogReadMilliVolts(MCP9700_PIN);

        delay(10);
    }

    float averageADC = adcSum / (float)NUM_SAMPLES;
    float averageVoltage_mV = voltageSum / (float)NUM_SAMPLES;

    float temperature_C = (averageVoltage_mV - 500.0) / 10.0;

    Serial.print("ADC: ");
    Serial.print(averageADC, 1);

    Serial.print(" | Voltage: ");
    Serial.print(averageVoltage_mV, 1);
    Serial.print(" mV");

    Serial.print(" | Temperature: ");
    Serial.print(temperature_C, 2);
    Serial.println(" °C");

    delay(1000);
}