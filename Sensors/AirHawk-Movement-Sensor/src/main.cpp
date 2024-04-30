#include <Arduino.h>
#include <CAN.h>
#include <WiFi.h>
#include <ArduinoJson.h>
#include <./state.cpp>
#include <Esp.h>
#include <SerialCommand.h>

const int PIR = 18;
const int LED_B = 2;
const int LED_G = 15;

const int CAN_RATE = 500E3;
const int CAN_ID = 0x1;
const int CAN_RX = 4;
const int CAN_TX = 5;
const bool CAN_ENABLED = false;

int connectedClients = 0;

DeviceState state;
SerialCommand commands;

class Commands {
  public:
    static void get_state() {
      Serial.println(state.serialize());
    }
};

void setup() {
  Serial.begin(115200);
  pinMode(PIR, INPUT);
  pinMode(LED_B, OUTPUT);
  pinMode(LED_G, OUTPUT);

  // Register commands
  commands.addCommand("get_state", Commands::get_state);

  // Configure state
  state.diskUsage = (float)ESP.getSketchSize() / (float)ESP.getFlashChipSize();
}

int lastState = LOW;
int lastTime = 0;
void loop() {
  int nowTime = millis();
  int present = digitalRead(PIR);

  if (present != lastState) {
    state.present = present;
    state.deltaTime = nowTime - lastTime;
    state.uptime = nowTime / 1000;

    if (present == HIGH) {
      digitalWrite(LED_B, HIGH);
      digitalWrite(LED_G, LOW);
      if (CAN_ENABLED) {
        CAN.beginPacket(CAN_ID);
        CAN.write('p');
        CAN.endPacket();
      }
    } else {
      digitalWrite(LED_B, LOW);
      digitalWrite(LED_G, HIGH);
      if (CAN_ENABLED) {
        CAN.beginPacket(CAN_ID);
        CAN.write('n');
        CAN.endPacket();
      }
    }

    lastState = present;
  }

  lastTime = nowTime;

  commands.readSerial();
  commands.clearBuffer();
}
