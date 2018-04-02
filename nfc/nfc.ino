#include <ESP8266WiFi.h>
#include <SPI.h>
#include "MFRC522.h"
#include <Adafruit_NeoPixel.h>
#include <PubSubClient.h>

/* wiring the MFRC522 to ESP8266 (ESP-12)
  RST     = GPIO5
  SDA(SS) = GPIO4
  MOSI    = GPIO13
  MISO    = GPIO12
  SCK     = GPIO14
  GND     = GND
  3.3V    = 3.3V
*/
const int RST_PIN   = 0;  // RST-PIN für RC522 - RFID - SPI - Modul GPIO5
const int SS_PIN    = 15; // SDA-PIN für RC522 - RFID - SPI - Modul GPIO4
const int LED_PIN   = 5;  //Pin which the leds are connected (GPIO5 = D1)

const int NUMPIXELS = 17; //Total number of Leds in each tile
const int GROUPSIZE = 4;  //Size of the leds in each group
const int SENSORTRESH = 50; //Treshhold for the data from piezo element
const int NFCTIMEOUT = 500;

const char *ssid =  "Ziggo78F5D45";     // change according to your Network - cannot be longer than 32 characters!
const char *pass =  "Sx7phx8fnkeP"; // change according to your Network
const char *mqtt_server = "192.168.178.40";
const char *NAME = "Tile0";
const char *TOPIC = "t0";
const char *LEDTOPIC = "led0";

MFRC522 mfrc522(SS_PIN, RST_PIN); // Create MFRC522 instance
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, LED_PIN, NEO_GRB + NEO_KHZ800);
WiFiClient espClient;
PubSubClient client(espClient);

int sensorValue;
bool foundCard = true;

long lastMsg = 0;
char msg[50];

int lastState = 0;
int readData;
MFRC522::StatusCode status; //variable to get card status

byte buffer[18];  //data transfer buffer (16+2 bytes data+CRC)
byte size = sizeof(buffer);

uint8_t pageAddr = 0x06;

void setup() {
  pixels.begin(); // This initializes the NeoPixel library.
  StartSequence();

  Serial.begin(115200);    // Initialize serial communications
  Serial.println(NAME);

  SPI.begin();           // Init SPI bus

  mfrc522.PCD_Init();    // Init MFRC522
  Serial.println(mfrc522.PCD_GetAntennaGain()); // gives me a 64 (00000010)
  mfrc522.PCD_SetAntennaGain(112); // set to max (00001110)
  Serial.println(mfrc522.PCD_GetAntennaGain()); //gives me the 112
  memcpy(buffer, "2", 1);

  WiFi.begin(ssid, pass);

  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  while ((WiFi.status() != WL_CONNECTED)) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(F("WiFi connected"));
  ColorAll(0, 255, 0);
}

void loop() {
  sensorValue = analogRead(A0);

  if (sensorValue >= SENSORTRESH) {
    sendSensor(sensorValue);
  }

  // Serial.println(sensorValue);
  // && mfrc522.PICC_ReadCardSerial()
  if ( mfrc522.PICC_IsNewCardPresent() || mfrc522.PICC_ReadCardSerial()) {
    // Show some details of the PICC (that is: the tag/card)
    //Serial.print(F("Card UID:"));
    //dump_byte_array(mfrc522.uid.uidByte, mfrc522.uid.size);
    //Serial.println();
    // Read data ***************************************************
    //Serial.println(F("Reading data ... "));
    //data in 4 block is readed at once.
    if (lastState == 0) {
      status = (MFRC522::StatusCode) mfrc522.MIFARE_Read(pageAddr, buffer, &size);
      if (status != MFRC522::STATUS_OK) {
        Serial.print(F("MIFARE_Read() failed: "));
        Serial.println(mfrc522.GetStatusCodeName(status));
        return;
      }

      Serial.print(F("Readed data: "));
      //Dump a byte array to Serial

      Serial.write(buffer[0]);

      Serial.println();
      readData = buffer[0];
      memset(buffer, 0, 18);
    }
    foundCard = true;


  }

  size = sizeof(buffer);

  long now = millis();
  if (now - lastMsg > NFCTIMEOUT) {
    if (!foundCard && lastState != 0) {
      sendNull();
      lastState = 0;
    } else if (foundCard && lastState != 1) {
      
      sendMsg(readData);
      lastState = 1;

    }
    foundCard = false;
    lastMsg = now;

  }

  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  delay(10);
}

void sendMsg(int ms) {
  snprintf (msg, 75, "a%ld", ms - 48);
  Serial.print("Publish message: ");
  Serial.println(msg);
  client.publish(TOPIC, msg);
}


void sendNull() {
  snprintf (msg, 75, "a%ld", 0);
  Serial.print("Publish message: ");
  Serial.println(msg);
  client.publish(TOPIC, msg);
}

void sendSensor(int ms) {
  snprintf (msg, 75, "s%ld", ms);
  Serial.print("Publish message: ");
  Serial.println(msg);
  client.publish(TOPIC, msg);
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect(NAME)) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.publish("outTopic", "hello world");
      // ... and resubscribe
      client.subscribe(LEDTOPIC);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  String r, g, b, t, d;
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < 3; i++) {
    Serial.print((char)payload[i]);
    r = r + (char)payload[i];
  }
  for (int i = 3; i < 6; i++) {
    Serial.print((char)payload[i]);
    g = g + (char)payload[i];
  }
  for (int i = 6; i < 9; i++) {
    Serial.print((char)payload[i]);
    b = b + (char)payload[i];
  }

  t = (char)payload[9];
  d = (char)payload[10];
  d += (char)payload[11];

  Serial.print(t.toInt());
  Serial.println(d.toInt());
  if (t.toInt() == 1)
    ColorAll(r.toInt(), g.toInt(), b.toInt());
  if (t.toInt() == 2)
    ColorPer(r.toInt(), g.toInt(), b.toInt(), 50);
  if (t.toInt() == 3)
    ColorGroup(r.toInt(), g.toInt(), b.toInt(), d.toInt());
  if (t.toInt() == 4)
    ColorLed(r.toInt(), g.toInt(), b.toInt(), d.toInt());
  //  Serial.println();
  //  Serial.println(r.toInt());
  //  Serial.println(g.toInt());
  //  Serial.println(b.toInt());

}

// Helper routine to dump a byte array as hex values to Serial
void dump_byte_array(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], HEX);
  }
}

void StartSequence() {
  ColorPer(255, 0, 0, 100);
  delay(500);
  ColorPer(0, 255, 0, 100);
  delay(500);
  ColorPer(0, 0, 255, 100);
  delay(500);
  ColorAll(255, 0, 0);
}

int DecodeR(byte* rgb) {
  String newR;
  for (int i = 0; i < 3; i++) {
    newR += (char)rgb[i];
  }
  return newR.toInt();
}

int DecodeG(byte* rgb) {
  String newG;
  for (int i = 0; i < 3; i++) {
    newG += (char)rgb[i];
  }
  return newG.toInt();
}

int DecodeB(byte* rgb) {
  String newB;
  for (int i = 0; i < 3; i++) {
    newB += (char)rgb[i];
  }
  return newB.toInt();
}


void ColorAll(int r, int g, int b) {
  for (int i = 0; i < NUMPIXELS; i++) {
    // pixels.Color takes RGB values, from 0,0,0 up to 255,255,255
    pixels.setPixelColor(i, pixels.Color(r, g, b)); // Moderately bright green color.
  }
  pixels.show(); // This sends the updated pixel color to the hardware.
}

void ColorLed(int r, int g, int b, int l) {
  pixels.setPixelColor(l, pixels.Color(r, g, b)); // Moderately bright green color.
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
