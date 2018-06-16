/*
 * --------------------------------------------------------------------------------------------------------------------
 * Example sketch/program showing how to read data from a PICC to serial.
 * --------------------------------------------------------------------------------------------------------------------
 * This is a MFRC522 library example; for further details and other examples see: https://github.com/miguelbalboa/rfid
 * 
 * Example sketch/program showing how to read data from a PICC (that is: a RFID Tag or Card) using a MFRC522 based RFID
 * Reader on the Arduino SPI interface.
 * 
 * When the Arduino and the MFRC522 module are connected (see the pin layout below), load this sketch into Arduino IDE
 * then verify/compile and upload it. To see the output: use Tools, Serial Monitor of the IDE (hit Ctrl+Shft+M). When
 * you present a PICC (that is: a RFID Tag or Card) at reading distance of the MFRC522 Reader/PCD, the serial output
 * will show the ID/UID, type and any data blocks it can read. Note: you may see "Timeout in communication" messages
 * when removing the PICC from reading distance too early.
 * 
 * If your reader supports it, this sketch/program will read all the PICCs presented (that is: multiple tag reading).
 * So if you stack two or more PICCs on top of each other and present them to the reader, it will first output all
 * details of the first and then the next PICC. Note that this may take some time as all data blocks are dumped, so
 * keep the PICCs at reading distance until complete.
 * 
 * @license Released into the public domain.
 * 
 * Typical pin layout used:
 * -----------------------------------------------------------------------------------------------
 *             MFRC522      Node    Arduino       Arduino   Arduino    Arduino          Arduino       
 *             Reader/PCD   MCU     Uno/101       Mega      Nano v3    Leonardo/Micro   Pro Micro
 * Signal      Pin          Pin     Pin           Pin       Pin        Pin              Pin
 * -----------------------------------------------------------------------------------------------
 * RST/Reset   RST          0       9             5         D9         RESET/ICSP-5     RST
 * SPI SS      SDA(SS)      15      10            53        D10        10               10
 * SPI MOSI    MOSI         13      11 / ICSP-4   51        D11        ICSP-4           16
 * SPI MISO    MISO         12      12 / ICSP-1   50        D12        ICSP-1           14
 * SPI SCK     SCK          14      13 / ICSP-3   52        D13        ICSP-3           15
 */

#include <ESP8266WiFi.h>
#include <DNSServer.h>
#include <ESP8266WebServer.h>
#include <WiFiManager.h> 

#include <PubSubClient.h>

#include "SPI.h" // SPI library
#include "MFRC522.h" // RFID library (https://github.com/miguelbalboa/rfid)

WiFiClient espClient;
PubSubClient mqttClient(espClient);

const char* default_mqtt_server = "server.tobernguyen.com";
//const char* default_mqtt_server = "10.0.0.230";
const char* default_mqtt_port = "1883";
char mqtt_server[255];
char mqtt_port[6];
char id[20];

int led = 2;

const char* public_topic = "pas/mqtt/rfid/user_scan";

const int pinRST = 0;
const int pinSDA = 15;
MFRC522 mfrc522(pinSDA, pinRST); // Set up mfrc522 on the Arduino

void configModeCallback (WiFiManager *myWiFiManager) {
  Serial.println("Entered config mode");
  Serial.println(WiFi.softAPIP());

  Serial.println(myWiFiManager->getConfigPortalSSID());
}

void setup() {
  pinMode(led, OUTPUT);
  digitalWrite(led, LOW);
  Serial.begin(115200); // open serial connection

  WiFiManager wifiManager;
  wifiManager.setAPCallback(configModeCallback);

  WiFiManagerParameter custom_mqtt_server("server", "mqtt server", default_mqtt_server, 40);
  WiFiManagerParameter custom_mqtt_port("port", "mqtt port", default_mqtt_port, 6);
  wifiManager.addParameter(&custom_mqtt_server); 
  wifiManager.addParameter(&custom_mqtt_port);

  wifiManager.resetSettings();
  if (!wifiManager.autoConnect("DONG_HM2")) {
    Serial.println("failed to connect, we should reset as see if it connects");
    delay(3000);
    ESP.reset();
    delay(5000);
  } 
  Serial.println("connected...wifi :)");

  strcpy(mqtt_server, custom_mqtt_server.getValue());
  strcpy(mqtt_port, custom_mqtt_port.getValue());
  mqttClient.setServer(mqtt_server, atoi(mqtt_port));
  mqttClient.setCallback(callback);
  
  Serial.println("");
  SPI.begin(); // open SPI connection
  Serial.println("SPI begin done!");
  mfrc522.PCD_Init(); // Initialize Proximity Coupling Device (PCD)
  Serial.println("Setup done!");
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
}

void reconnect() {
  // Đợi tới khi kết nối
  while (!mqttClient.connected()) {
    Serial.print("Attempting MQTT connection...");

    if (mqttClient.connect("ESP8266Client")) {
      Serial.println("Connected MQTT server!");
//      mqttClient.publish(public_topic, "hello dong");
    } else {
      Serial.print("failed, rc=");
      Serial.print(mqttClient.state());
      Serial.println(" try again in 3 seconds");
      delay(3000);
    }
  }
}

void beep() {
  analogWrite(4, 500);
  delay(100);
  analogWrite(4, -1);
}

void loop() {

  analogWrite(4, -1);

  if (!mqttClient.connected()) {
    digitalWrite(led, LOW);
    reconnect();
  }
  digitalWrite(led, HIGH);
  
  mqttClient.loop();
  
  if (mfrc522.PICC_IsNewCardPresent()) { // (true, if RFID tag/card is present ) PICC = Proximity Integrated Circuit Card
    Serial.println("has new card");
    if(mfrc522.PICC_ReadCardSerial()) { // true, if RFID tag/card was read
      String content= "";
      Serial.print("RFID TAG ID:");
      for (byte i = 0; i < mfrc522.uid.size; ++i) { // read id (in parts)
        Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
        Serial.print(mfrc522.uid.uidByte[i], HEX);
        content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
        content.concat(String(mfrc522.uid.uidByte[i], HEX));
//        Serial.print(mfrc522.uid.uidByte[i], HEX); // print id as hex values
//        Serial.print(" "); // add space between hex blocks to increase readability
      }
      content.toUpperCase();
      content = content.substring(1);
      Serial.println();
      Serial.print("Content: ");
      Serial.print(content);
//      strcpy(id, content);
      mqttClient.publish(public_topic, content.c_str());
      beep();
      Serial.println();
      delay(2000);
    }
  }
}
