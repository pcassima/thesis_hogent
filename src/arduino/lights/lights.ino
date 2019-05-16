/* Racing Lights (written for nodeMCU, esp8266)
 * 
 * This program controlls the racing lights.
 * It will start the countdown when it receives a commando.
 * When it's green it will send a commando back to enable driving.
 * For the hardware: RGB LED's with blue not connected
 * 
 * Written by J. Sarrazyn
 */

// Libraries
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// Set WiFi and pubsub client name
WiFiClient ClientNode;
PubSubClient client(ClientNode);

// WiFi network ssid and password also the status
const char* ssid = "StageSupernet";
const char* password = "StageSupernet";
int status = WL_IDLE_STATUS;

// Mqtt topic
const char* Topic = "vroom";

// Name of this device
const char* thisObject = "21";

// Mqtt server and port
char* mqttServer = "192.168.1.5";
int mqttPort = 1881;

// Message array to save the incomming message to
byte MessageByte[9];

// Message byte array to enable stering on another device
byte sendMessage[9] = {60, 21, 1, 0, 11, 0, 1, 0};

// RGB connection red
byte red1 = 16;
byte red2 = 4;
byte red3 = 2;
byte red4 = 12;

// RGB connection green
byte green1 = 5;
byte green2 = 0;
byte green3 = 14;
byte green4 = 13;

// Function to read the incomming message
void callback(char* topic, byte* payload, unsigned int length) {

  // Set every incomming byte to a place in the array
  for (int i = 0; i < length; i++) {
    MessageByte[i] = payload[i];
  }
}

// Function to connect to the WiFi and mqtt
void ConnectWiFi() {

  // Start WiFi connection
  status = WiFi.begin(ssid, password);

  // Connecting to the WiFi (for debug)
   // Serial.print("Connecting to WiFi");

  // While not connected to WiFi
  while (WiFi.status() != WL_CONNECTED) {

    // Wait 500 ms
    delay(500);

    // Connecting (for debug)
     // Serial.print(".");
  }

  // Connected (for debug)
   // Serial.println("");
   // Serial.println("Connected to the WiFi network");

  // Connected with (for debug)
   // Serial.print("With ip: ");
   // Serial.println(WiFi.localIP());


  // Set mqtt server (port) and calback
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);

  // While not connected to mqtt
  while (!client.connected()) {

    // Wait 500 ms
    delay(500);

    // Connecting (for debug)
     // Serial.println("Connecting to MQTT...");

    // If connected to the mqtt
    if (client.connect(thisObject)) {

      // Connected to the mqtt (for debug)
       // Serial.println("Connected");

      // Wait 200 ms
      delay(200);
    }

    // If not connected to the mqtt
    else {

      // Error (for debug)
       // Serial.print("failed with state ");
       // Serial.println(client.state());

      // Wait 2000 ms
      delay(2000);
    }
  }

  // Subscibe to the set topic
  client.subscribe(Topic);

  // Subscribed to the topic:... (for debug)
   // Serial.print("Subscribed to the topic ");
   // Serial.println(Topic);
}

void setup() {
  // Setting the pinmode for the LED's
  pinMode(red1, OUTPUT);
  pinMode(red2, OUTPUT);
  pinMode(red3, OUTPUT);
  pinMode(red4, OUTPUT);
  pinMode(green1, OUTPUT);
  pinMode(green2, OUTPUT);
  pinMode(green3, OUTPUT);
  pinMode(green4, OUTPUT);

  // Making sure the lights are out
  lightsOut();

  // Start serial port (for debug)
  // Serial.begin(115200);

  // Wait one second
  delay(1000);

  // Start the connect to WiFi and mqtt function
  ConnectWiFi();
}

void loop() {

  // Keep reading all incomming messages
  client.loop();

  // Check if the message is for this device
  if (MessageByte[0] == 21) {

    // Making sure the message is only read ones
    MessageByte[0] = 0;
    
    // Checking what the function number is
    if (MessageByte[2] == 1) {

      // Using a delay that has been send by the controller
      int Delay;
      Delay = (MessageByte[6] * 4);

      // Start the countdown
      // First LED red and delay
      digitalWrite(red1, HIGH);
      delay(Delay);
      
      // Second LED red and delay
      digitalWrite(red2, HIGH);
      delay(Delay);

      // Third LED red and delay
      digitalWrite(red3, HIGH);
      delay(Delay);

      // Fourth LED red and delay
      digitalWrite(red4, HIGH);
      delay(Delay);
      
      // All LED's red out
      digitalWrite(red1, LOW);
      digitalWrite(red2, LOW);
      digitalWrite(red3, LOW);
      digitalWrite(red4, LOW);

      // All LED's green on
      digitalWrite(green1, HIGH);
      digitalWrite(green2, HIGH);
      digitalWrite(green3, HIGH);
      digitalWrite(green4, HIGH);

      // Send message for enabling the steering
      client.publish(Topic, sendMessage, 8);
    }
    else if (MessageByte[2] == 0) {

      // Kill the lights
      lightsOut();
    }
  }
}

// This is to kill the lights
void lightsOut() {

  // Red out
  digitalWrite(red1, LOW);
  digitalWrite(red2, LOW);
  digitalWrite(red3, LOW);
  digitalWrite(red4, LOW);

  // Green out
  digitalWrite(green1, LOW);
  digitalWrite(green2, LOW);
  digitalWrite(green3, LOW);
  digitalWrite(green4, LOW);
}

