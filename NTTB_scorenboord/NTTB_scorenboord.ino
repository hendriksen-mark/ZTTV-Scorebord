#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <WiFiManager.h>

ESP8266WebServer server(80);

#define PROJECT_NAME "NTTB"


void setup() {
  Serial.begin(19200);
  WiFi.mode(WIFI_STA);
  WiFiManager wifiManager;
  wifiManager.setConfigPortalTimeout(120);
  wifiManager.autoConnect(PROJECT_NAME);
  wifiManager.setConnectTimeout(30);
  WiFi.hostname(PROJECT_NAME);

  //server.on("/sbsetting", sbsetting);
  //server.on("/sblogo", sblogo);
  //server.on("/sbdata", sbdata);
  server.onNotFound(handleNotFound);

  server.begin();
}

void loop() {
  server.handleClient();
}

void handleNotFound() {
  Serial.printf("method: %s, num args: %d, on url: %s \n",(server.method() == HTTP_GET) ? "GET" : "POST", server.args(), server.uri());
  for (int i = 0; i < server.args(); i++) {
    Serial.printf("args: %s = %s\n", server.argName(i).c_str(), server.arg(i).c_str());
  }
  server.send(200, "text/plain", "test headers");
}

void sbsetting() {
  Serial.printf("num args: %d, on url: /sbsetting \n",server.args());
  for (int i = 0; i < server.args(); i++) {
    Serial.printf("args: %s = %s\n", server.argName(i).c_str(), server.arg(i).c_str());
  }
  server.send(200, "text/plain", "test headers");
}

void sblogo() {
  Serial.printf("num args: %d, on url: /sblogo \n",server.args());
  for (int i = 0; i < server.args(); i++) {
    Serial.printf("args: %s = %s\n", server.argName(i).c_str(), server.arg(i).c_str());
  }
  server.send(200, "text/plain", "test headers");
}

void sbdata() {
  Serial.printf("num args: %d, on url: /sbdata \n",server.args());
  for (int i = 0; i < server.args(); i++) {
    Serial.printf("args: %s = %s\n", server.argName(i).c_str(), server.arg(i).c_str());
  }
  server.send(200, "text/plain", "test headers");
}
