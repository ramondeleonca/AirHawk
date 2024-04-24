#include <Arduino.h>
#include <CAN.h>

const int PIR = 4;

const int CAN_ID = 1;
const int CAN_TX = 16;
const int CAN_RX = 17;
const int CAN_RATE = 5000E3;

const int LED_B = 2;
const int LED_G = 15;

void setup() {
  Serial.begin(115200);

  CAN.setPins(CAN_RX, CAN_TX);
  CAN.begin(CAN_RATE);

  CAN.beginPacket(CAN_ID);
  CAN.write(1);
  CAN.endPacket();

  pinMode(PIR, INPUT);
  pinMode(LED_B, OUTPUT);
  pinMode(LED_G, OUTPUT);
}

int lastState = LOW;
void loop() {
  int presence = digitalRead(PIR);

  if (presence == HIGH) {
    digitalWrite(LED_B, HIGH);
    digitalWrite(LED_G, LOW);
    Serial.println("PRESENCE");
  } else {
    digitalWrite(LED_B, LOW);
    digitalWrite(LED_G, HIGH);
    Serial.println("NOMOTION");
  }

  if (presence != lastState) {
    CAN.beginPacket(CAN_ID);
    CAN.write(presence);
    CAN.endPacket();
    lastState = presence;
  }

  delay(100);
}
