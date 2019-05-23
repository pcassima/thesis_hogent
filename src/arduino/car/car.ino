/* Car (written for arduino mega)
 *  
 * This program is for controlling the car from a mqtt network.
 * If you use this program make sure their is only one client with this name.
 * The speed of the car isn't  controlled by a max PWM in this program.
 * To change the speed use the controller program.   
 * 
 * Written by J. Sarrazyn
*/

// Libraries
#include <WiFi101.h>
#include <PubSubClient.h>

// Set WiFi and pubsub client name
WiFiClient ClientMega;
PubSubClient client(ClientMega);

// WiFi network ssid and password also the status
const char* ssid = "StageSupernet";
const char* password = "StageSupernet";
int status = WL_IDLE_STATUS;

// Mqtt topic
const char* Topic = "vroom";

// Name of this car
byte thisCar = 20;

// Mqtt server and port
char* mqttServer = "192.168.1.5";
int mqttPort = 1881;

// Message array to save the incomming message to
byte MessageByte[8];

// Current speed of the car
byte currentSpeed = 0;

// Pin numbers for the PWM, left/right and standby
byte PWMleft = 44;
byte left2 = 40;
byte left1 = 41;
byte STBY = 47;
byte right1 = 43;
byte right2 = 42;
byte PWMright = 46;

void setup() {
  // Start serial port (for debug)
  // Serial.begin(115200);

  // Setting the pins for the WiFi
  WiFi.setPins(22, 23, 24);

  // Wait one second
  delay(1000);

  // Setting the standby pin high to enable the motors
  digitalWrite(STBY, HIGH);

  // Start the connect to WiFi and mqtt function
  ConnectWiFi();
}

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
    if (client.connect(thisCar)) {

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

void loop() {

  // Keep reading all incomming messages
  client.loop();

  // Check if the message is for this car
  if (MessageByte[0] == thisCar) {

    // Making sure the message is only read ones
    MessageByte[0] = 0;

    // Checking what the function number is
    if (MessageByte[2] == 0) {

      // Set speed to 0 en stop the car
      currentSpeed = 0;
      Stop();

      // (for debug)
       // Serial.println("Stop");
    }
    else if (MessageByte[2] == 1) {

      // Set speed to received speed en go forward
      currentSpeed = MessageByte[6];
      Forward(currentSpeed);

      // (for debug)
       // Serial.println("Forward");
    }
    else if (MessageByte[2] == 2) {

      // Set speed to received speed en go back
      currentSpeed = MessageByte[6];
      Back(currentSpeed);

      // (for debug)
       // Serial.println("Back");
    }
    else if (MessageByte[2] == 3) {

      // Go left with reveived speed
      Left(MessageByte[6]);

      // (for debug)
       // Serial.println("Left");
    }
    else if (MessageByte[2] == 4) {

      // Go right with received speed
      Right(MessageByte[6]);

      // (for debug)
       // Serial.println("Right");
    }
    else if (MessageByte[2] == 5 or MessageByte[2] == 6) {

      //Reset the speed to the previous speed
      setPWM(currentSpeed, currentSpeed);
    }

    /* (for debug)
      else if (MessageByte[2] == 5) {
        Serial.println("Left stop");
      }
      else if (MessageByte[2] == 6) {
        Serial.println("Right stop");
      }*/
  }
}

void Stop() {

  //stop the car => PWM = 0
  setPWM(0, 0);
}

void Forward(byte PWM) {

  // Left motor turn forward
  digitalWrite(left1, HIGH);
  digitalWrite(left2, LOW);

  // Right motor turn forward
  digitalWrite(right1, HIGH);
  digitalWrite(right2, LOW);

  // Set speed left and right
  setPWM(PWM, PWM);
}

void Back(byte PWM) {

  // Left motor turn back
  digitalWrite(left1, LOW);
  digitalWrite(left2, HIGH);

  // Right motor turn back
  digitalWrite(right1, LOW);
  digitalWrite(right2, HIGH);

  // Set speed left and right
  setPWM(PWM, PWM);
}

void Left(byte PWM) {

  // Calculate the speed to turn (motor right)
  int turnSpeed;
  turnSpeed = currentSpeed - PWM;

  // If turn speed is smaller than 0
  if (turnSpeed < 0) {

    // Right motor turn forward
    digitalWrite(right1, HIGH);
    digitalWrite(right2, LOW);

    // Set speed left and right
    setPWM(0, PWM);
  }
  else {

    // Set speed left and right
    setPWM(turnSpeed, currentSpeed);
  }
}

void Right(byte PWM) {

  // Calculate the speed to turn (motor right)
  int turnSpeed;
  turnSpeed = currentSpeed - PWM;

  // If turn speed is smaller than 0
  if (turnSpeed < 0) {

    // Left motor turn forward
    digitalWrite(left1, HIGH);
    digitalWrite(left2, LOW);

    // Set speed left and right
    setPWM(PWM, 0);
  }
  else {

    // Set speed left and right
    setPWM(currentSpeed, turnSpeed);
  }
}

void setPWM(byte PWMLeft, byte PWMRight) {

  // Write the PWM values to the motors
  analogWrite(PWMleft, PWMLeft);
  analogWrite(PWMright, PWMRight);

  // PWM values (for debug)
   // Serial.println(PWMLeft);
   // Serial.println(PWMRight);
}


