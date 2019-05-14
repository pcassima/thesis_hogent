#include <ESP8266WiFi.h>
#include <PubSubClient.h>

WiFiClient ClientNode;
PubSubClient client(ClientNode);

const char* ssid = "StageSupernet";
const char* password = "StageSupernet";
int status = WL_IDLE_STATUS;

const char* Topic = "vroom";
const char* thisObject = "21";

char* mqttServer = "192.168.1.5";
int mqttPort = 1881;

byte MessageByte[9];
byte prevMessageByte = 9;

byte sendMessage[9] = {60, 21, 1, 0, 11, 0, 1, 0};

void callback(char* topic, byte* payload, unsigned int length) {

  for (int i = 0; i < length; i++) {
    MessageByte[i] = payload[i];
  }
  Serial.println("received message");
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

  pinMode(16, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(0, OUTPUT);
  pinMode(2, OUTPUT);
  pinMode(14, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);

  lightsOut();

  Serial.begin(115200);

  delay(1000);

  ConnectWiFi();
}

void loop() {
  // put your main code here, to run repeatedly:
  client.loop();

  prevMessageByte = MessageByte[2];

  if (MessageByte[0] == 21) {

    if (MessageByte[2] == 1) {

      int Delay;

      Delay = (MessageByte[6] * 4);

      digitalWrite(16, HIGH);
      delay(Delay);
      digitalWrite(4, HIGH);
      delay(Delay);
      digitalWrite(2, HIGH);
      delay(Delay);
      digitalWrite(12, HIGH);
      delay(Delay);

      digitalWrite(16, LOW);
      digitalWrite(4, LOW);
      digitalWrite(2, LOW);
      digitalWrite(12, LOW);

      digitalWrite(5, HIGH);
      digitalWrite(0, HIGH);
      digitalWrite(14, HIGH);
      digitalWrite(13, HIGH);

      client.publish(Topic, sendMessage, 8);
    }

    else if (MessageByte[2] == 0) {

      lightsOut();
    }
  }
}

void lightsOut() {

  digitalWrite(16, LOW);
  digitalWrite(4, LOW);
  digitalWrite(2, LOW);
  digitalWrite(12, LOW);

  digitalWrite(5, LOW);
  digitalWrite(0, LOW);
  digitalWrite(14, LOW);
  digitalWrite(13, LOW);
}

