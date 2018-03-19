/*
  Many thanks to nikxha from the ESP8266 forum
*/

#include <ESP8266WiFi.h>
#include <SPI.h>
#include "MFRC522.h"
#include <WiFiUdp.h>
#include <OSCMessage.h>
#include <Adafruit_NeoPixel.h>
/* wiring the MFRC522 to ESP8266 (ESP-12)
  RST     = GPIO5
  SDA(SS) = GPIO4
  MOSI    = GPIO13
  MISO    = GPIO12
  SCK     = GPIO14
  GND     = GND
  3.3V    = 3.3V
*/

#define RST_PIN         0  // RST-PIN für RC522 - RFID - SPI - Modul GPIO5 
#define SS_PIN          15   // SDA-PIN für RC522 - RFID - SPI - Modul GPIO4 
#define LED_PIN         2
#define NUMPIXELS       3


int GROUPSIZE = 3;

int sensorValue;


const unsigned int outPort = 9999;
IPAddress outIp(192, 168, 43, 182);

WiFiUDP Udp;

//create new osc message
OSCMessage global_mes;

const char *ssid =  "test";     // change according to your Network - cannot be longer than 32 characters!
const char *pass =  "testtest"; // change according to your Network

MFRC522 mfrc522(SS_PIN, RST_PIN); // Create MFRC522 instance

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, LED_PIN, NEO_RGB + NEO_KHZ800);

void StartSequence() {
  ColorPer(255, 0, 0, 100);
  delay(500);
  ColorPer(0, 255, 0, 100);
  delay(500);
  ColorPer(0, 0, 255, 100);
  delay(500);
  ColorAll(255, 0, 0);

}

void ColorAll(int r, int g, int b) {
  for (int i = 0; i < NUMPIXELS; i++) {
    // pixels.Color takes RGB values, from 0,0,0 up to 255,255,255
    pixels.setPixelColor(i, pixels.Color(r, g, b)); // Moderately bright green color.
  }
  pixels.show(); // This sends the updated pixel color to the hardware.
}

void ColorPer(int r, int g, int b, int del) {
  for (int i = 0; i < NUMPIXELS; i++) {
    // pixels.Color takes RGB values, from 0,0,0 up to 255,255,255
    pixels.setPixelColor(i, pixels.Color(r, g, b)); // Moderately bright green color.
    pixels.show(); // This sends the updated pixel color to the hardware.
    delay(del);
  }
}

void ColorGroup(int r, int g, int b, int group) {
  for (int i = GROUPSIZE * group; i < GROUPSIZE * group + GROUPSIZE; i++) {
    // pixels.Color takes RGB values, from 0,0,0 up to 255,255,255
    pixels.setPixelColor(i, pixels.Color(r, g, b)); // Moderately bright green color.
    pixels.show(); // This sends the updated pixel color to the hardware.
    delay(100);
  }
}

void setup() {
  pinMode(5, INPUT);
  delay(500);

  pixels.begin(); // This initializes the NeoPixel library.

  Serial.begin(115200);    // Initialize serial communications
  delay(250);
  Serial.println(F("Booting...."));

  StartSequence();

  SPI.begin();           // Init SPI bus
  mfrc522.PCD_Init();    // Init MFRC522
  mfrc522.PCD_ClearRegisterBitMask(mfrc522.RFCfgReg, (0x07 << 4));
  mfrc522.PCD_SetRegisterBitMask(mfrc522.RFCfgReg, (0x07 << 4));

  WiFi.begin(ssid, pass);

  int retries = 0;
  while ((WiFi.status() != WL_CONNECTED) && (retries < 10)) {
    retries++;
    delay(500);
    Serial.print(".");
  }
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println(F("WiFi connected"));
    ColorAll(0, 255, 0);
  }

  Serial.println(F("Ready!"));
  Serial.println(F("======================================================"));
  Serial.println(F("Scan for Card and print UID:"));

  Udp.begin(8888);
}

void loop() {
  sensorValue = digitalRead(5);

  if (sensorValue == HIGH) {
    for (int i = 0; i < NUMPIXELS; i++) {
      // pixels.Color takes RGB values, from 0,0,0 up to 255,255,255
      pixels.setPixelColor(i, pixels.Color(0, 150, 0)); // Moderately bright green color.
    }
    pixels.show(); // This sends the updated pixel color to the hardware.
  } else {
    for (int i = 0; i < NUMPIXELS; i++) {
      // pixels.Color takes RGB values, from 0,0,0 up to 255,255,255
      pixels.setPixelColor(i, pixels.Color(150, 0, 0)); // Moderately bright green color.
    }
    pixels.show(); // This sends the updated pixel color to the hardware.
  }

  //Serial.println(sensorValue);
  // Look for new cards
  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
    delay(50);
    // Show some details of the PICC (that is: the tag/card)
    Serial.print(F("Card UID:"));
    dump_byte_array(mfrc522.uid.uidByte, mfrc522.uid.size);
    Serial.println();
    ColorAll(0, 255, 0);
    delay(200);
    ColorAll(0, 255, 0);
    delay(200);
    ColorAll(0, 255, 0);
    delay(200);
    ColorAll(0, 255, 0);
  }
}

// Helper routine to dump a byte array as hex values to Serial
void dump_byte_array(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], HEX);
  }
}
