#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <Arduino_JSON.h>

const int greenLED = 16;  //D0
const int redLED = 5;     //D1
const int blueLED = 4;    //D2

const char* ssid = "SSID";
const char* password = "PASS";

const char* serverName = "ADDRESS";


unsigned long lastTime = 0;
unsigned long timerDelay = 5000;

String led_values;
float sensorReadingsArr[3];

void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());

}

void loop() {
  if ((millis() - lastTime) > timerDelay) {
    //Check WiFi connection status
    if (WiFi.status() == WL_CONNECTED) {
      led_values = httpGETRequest(serverName);
      Serial.println(led_values);
      if (led_values != "fail") {

        int array[3];
        int r = 0, t = 0;

        for (int i = 0; i < led_values.length(); i++) {
          if (led_values[i] == ',' || led_values[i] == '[') {
            if (i - r > 1) {
              array[t] = led_values.substring(r, i).toInt();
              t++;
            }
            r = (i + 1);
          }
          if (t >= 3) {
            break;
          }
        }
        for (int k = 0; k <= 2; k++) {
          Serial.println(array[k]);
        }
        pinMode(redLED, OUTPUT);
        pinMode(greenLED, OUTPUT);
        pinMode(blueLED, OUTPUT);

        analogWrite(redLED, 255-array[0]);
        analogWrite(greenLED, 255-array[1]);
        analogWrite(blueLED, 255-array[2]);
      }
    } else {
      Serial.println("WiFi Disconnected");
    }
    lastTime = millis();
  }
}

String httpGETRequest(const char* serverName) {
  WiFiClient client;
  HTTPClient http;

  http.begin(client, serverName);

  int httpResponseCode = http.GET();

  String payload = "{}";

  if (httpResponseCode == 200) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    payload = http.getString();
  } else {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
    payload = "fail";
  }
  http.end();

  return payload;
}
