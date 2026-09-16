/*
  Smart Industrial Monitor - ESP8266 -> Public Render Website
  Replace WIFI_SSID, WIFI_PASSWORD and SERVER_URL.
  Example SERVER_URL:
  https://your-service.onrender.com/api/sensor-data
*/

#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>

const char* WIFI_SSID = "YOUR_WIFI_NAME";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";
const char* SERVER_URL = "https://YOUR-APP.onrender.com/api/sensor-data";

void setup() {
  Serial.begin(115200);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("NodeMCU IP: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    WiFiClientSecure client;
    client.setInsecure(); // Prototype only; use certificate validation for production.

    HTTPClient http;
    http.begin(client, SERVER_URL);
    http.addHeader("Content-Type", "application/json");

    // Replace these demo values with real sensor readings.
    StaticJsonDocument<256> doc;
    doc["temperature"] = 34.6;
    doc["humidity"] = 61.0;
    doc["vibration"] = 1.2;
    doc["current"] = 2.4;
    doc["voltage"] = 12.1;
    doc["gas"] = 125.0;

    String body;
    serializeJson(doc, body);

    int code = http.POST(body);
    Serial.print("HTTP response: ");
    Serial.println(code);
    http.end();
  }
  delay(3000);
}
