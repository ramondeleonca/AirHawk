#include <Arduino.h>
#include <CAN.h>

const int PIR = 18;
const int LED_B = 2;
const int LED_G = 15;

const int CAN_RATE = 500E3;
const int CAN_ID = 0x1;
const int CAN_RX = 4;
const int CAN_TX = 5;
const bool CAN_ENABLED = true;

void setup() {
  Serial.begin(115200);
  pinMode(PIR, INPUT);
  pinMode(LED_B, OUTPUT);
  pinMode(LED_G, OUTPUT);

  CAN.setPins(CAN_RX, CAN_TX);
  int success = CAN.begin(CAN_RATE);
  if (!success) {
    Serial.println("CAN initialization failed");
  } else Serial.println("CAN initialized");
  Serial.println(success);

  CAN.beginPacket(CAN_ID);
  CAN.write('u');
  CAN.write('p');
  CAN.endPacket();
  Serial.println("CAN packet sent");
}

int lastState = LOW;
void loop() {
  int presence = digitalRead(PIR);

  if (presence != lastState) {
    if (presence == HIGH) {
      digitalWrite(LED_B, HIGH);
      digitalWrite(LED_G, LOW);
      Serial.println("PRESENCE");
      if (CAN_ENABLED) {
        CAN.beginPacket(CAN_ID);
        CAN.write('p');
        CAN.endPacket();
        Serial.println("CAN packet sent");
      }
    } else {
      digitalWrite(LED_B, LOW);
      digitalWrite(LED_G, HIGH);
      Serial.println("NOMOTION");
      if (CAN_ENABLED) {
        CAN.beginPacket(CAN_ID);
        CAN.write('n');
        CAN.endPacket();
        Serial.println("CAN packet sent");
      }
    }
    lastState = presence;
  }
}
