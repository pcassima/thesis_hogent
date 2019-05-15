/* Reader (written for nodeMCU, esp8266)
 *  
 * This program reads every incomming message an decodes it.
 * 
 * Written by J. Sarrazyn
 */

#include <ESP8266WiFi.h>
#include <PubSubClient.h>

WiFiClient ClientNode;
PubSubClient client(ClientNode);

const char* ssid = "StageSupernet";
const char* password = "StageSupernet";
int status = WL_IDLE_STATUS;

const char* Topic = "vroom";
const char* thisObject = "22";

char* mqttServer = "192.168.1.5";
int mqttPort = 1881;

byte MessageByte[8];
byte prevMessageByte20 = 0;
byte prevMessageByte21 = 0;
byte prevMessageByte60 = 0;
byte prevMessageByte61 = 0;

String line ("################################################");

void callback(char* topic, byte* payload, unsigned int length) {

  for (int i = 0; i < length; i++) {
    MessageByte[i] = payload[i];
  }
}

void ConnectWiFi() {

  status = WiFi.begin(ssid, password);

  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");

  Serial.println("Connected to the WiFi network");

  Serial.print("With ip: ");
  Serial.println(WiFi.localIP());


  // mqtt
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);

  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");

    if (client.connect(thisObject)) {
      Serial.println("Connected");

    }
    else {
      Serial.print("failed with state ");
      Serial.println(client.state());
      delay(2000);
    }
  }
  client.subscribe(Topic);

  Serial.print("Subscribed to the topic ");
  Serial.println(Topic);
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  delay(1000);

  ConnectWiFi();
}

void loop() {
  // put your main code here, to run repeatedly:
  client.loop();

  if (MessageByte[0] == 20) {
    if (prevMessageByte20 != MessageByte[2]) {
      
      prevMessageByte20 = MessageByte[2];

      Serial.print("Message:  ");
      for (int i = 0; i < 8; i++) {
        Serial.print(MessageByte[i]);
        Serial.print("//");
      }
      Serial.println("");

      Serial.print("From:     ");
      switch (MessageByte[1]){
        case 20:
        Serial.println("Car");
        break;

        case 21:
        Serial.println("Lights");
        break;

        case 60:
        Serial.println("Controller");
        break;

        case 61:
        Serial.println("Vision");
        break;
      }
      Serial.print("To:       ");
      Serial.println("Car");
      
      Serial.print("What:     ");

      switch (MessageByte[2]) {
        case 0:
          Serial.println("Stop");
          break;
          
        case 1:
          Serial.println("forward");
          break;
          
        case 2:
          Serial.println("Back");
          break;
          
        case 3:
          Serial.println("left");
          break;
          
        case 4:
          Serial.println("Right");
          break;
          
        case 5:
          Serial.println("Left stop");
          break;
          
        case 6:
          Serial.println("Right stop");
          break;
      }

      Serial.print("Speed:    ");
      Serial.println(MessageByte[6]);

      Serial.println(line);
    }
  }

  if (MessageByte[0] == 21) {
    if (prevMessageByte21 != MessageByte[2]) {
      
      prevMessageByte21 = MessageByte[2];

      Serial.print("Message:  ");
      for (int i = 0; i < 8; i++) {
        Serial.print(MessageByte[i]);
        Serial.print("//");
      }
      Serial.println("");

      Serial.print("From:     ");
      switch (MessageByte[1]){
        case 20:
        Serial.println("Car");
        break;

        case 21:
        Serial.println("Lights");
        break;

        case 60:
        Serial.println("Controller");
        break;

        case 61:
        Serial.println("Vision");
        break;
      }
      Serial.print("To:       ");
      Serial.println("Lights");

      Serial.print("What:     ");

      switch (MessageByte[2]) {
        case 0:
          Serial.println("Lights out");
          prevMessageByte60 = 0;
          break;
          
        case 1:
          Serial.println("Start countdown");
          break;
      }

      Serial.println(line);
    }
  }

  if (MessageByte[0] == 60) {
    if (prevMessageByte60 != MessageByte[2]) {
      
      prevMessageByte60 = MessageByte[2];

      Serial.print("Message:  ");
      for (int i = 0; i < 8; i++) {
        Serial.print(MessageByte[i]);
        Serial.print("//");
      }
      Serial.println("");

      Serial.print("From:     ");
      switch (MessageByte[1]){
        case 20:
        Serial.println("Car");
        break;

        case 21:
        Serial.println("Lights");
        break;

        case 60:
        Serial.println("Controller");
        break;

        case 61:
        Serial.println("Vision");
        break;
      }
      Serial.print("To:       ");
      Serial.println("Controller");

      Serial.print("What:     ");

      switch (MessageByte[2]) {
        case 0:
          Serial.println("Disable steering");
          break;
          
        case 1:
          Serial.println("Enable steering");
          break;
      }

      Serial.println(line);
    }
  }

  if (MessageByte[0] == 61) {
    if (prevMessageByte61 != MessageByte[2]) {
      
      prevMessageByte61 = MessageByte[2];

      Serial.print("Message:  ");
      for (int i = 0; i < 8; i++) {
        Serial.print(MessageByte[i]);
        Serial.print("//");
      }
      Serial.println("");

      Serial.print("From:     ");
      switch (MessageByte[1]){
        case 20:
        Serial.println("Car");
        break;

        case 21:
        Serial.println("Lights");
        break;

        case 60:
        Serial.println("Controller");
        break;

        case 61:
        Serial.println("Vision");
        break;
      }
      Serial.print("To:       ");
      Serial.println("Vision");

      Serial.print("What:     ");

      Serial.println("Unknown");
        
      Serial.println(line);
    }
  }
}
