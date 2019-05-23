/* Joystick
 *
 * This program is used to read analog value and send it over the mqtt network.
 * It works best on a arduino mega.
 * But this is made for the arduino Leonardo.
 * That is why not all the functions are available.
 *
 * Written by J. Sarrazyn
 */



#include <PubSubClient.h>
#include <WiFi101.h>

WiFiClient Joystick;

PubSubClient client(Joystick);

//ssid and password for the WiFi
/*const char* ssid = "StageSupernet";
const char* password =  "StageSupernet";*/
int status = WL_IDLE_STATUS;

//const char* Topic = "vroom";
byte thisDevice = 22;

//IP adress of the mqtt server
/*char* mqttServer = "192.168.1.5";
//Port of the mqtt server
int mqttPort = 1881;*/

// Message array to save the incomming message to
byte MessageByte[8];

// Array to send
byte sendDataValue[8] = {20, 22, 10, 0, 11, 0, 0, 0};

// Ports for the joystick
//int Y_speed = A4;
//int X_turn = A5;

// Speed and turn value
int speed_val;
int turn_val;

// Previous speed and turn value
int prev_speed_val;
int prev_turn_val;

// For checking the change
int analog_Y_val;
int analog_X_val;

// Function to read the incomming message
/*void callback(char* topic, byte* payload, unsigned int length) {

  // Set every incomming byte to a place in the array
  for (int i = 0; i < length; i++) {
    MessageByte[i] = payload[i];
  }
}*/

void ConnectWiFi() {

  // Start WiFi connection
  status = WiFi.begin("StageSupernet", "StageSupernet");

  // Connecting to the WiFi (for debug)
  // //Serial.print("Connecting to WiFi");

  // While not connected to WiFi
  while (WiFi.status() != WL_CONNECTED) {

    // Wait 500 ms
    delay(500);

    // Connecting (for debug)
    // //Serial.print(".");
  }

  // Connected (for debug)
  // //Serial.println("");
  // //Serial.println("Connected to the WiFi network");

  // Connected with (for debug)
  // //Serial.print("With ip: ");
  // //Serial.println(WiFi.localIP());


  // Set mqtt server (port) and calback
  client.setServer("192.168.1.5", 1881);
  //client.setCallback(callback);

  // While not connected to mqtt
  while (!client.connected()) {

    // Wait 500 ms
    delay(500);

    // Connecting (for debug)
    // //Serial.println("Connecting to MQTT...");

    // If connected to the mqtt
    if (client.connect(thisDevice)) {

      // Connected to the mqtt (for debug)
      // //Serial.println("Connected");

      // Wait 200 ms
      delay(200);
    }

    // If not connected to the mqtt
    /*else {

      // Error (for debug)
      // //Serial.print("failed with state ");
      // //Serial.println(client.state());

      // Wait 2000 ms
      delay(2000);
    }*/
  }

  // Subscibe to the set topic
  client.subscribe("vroom");

  // Subscribed to the topic:... (for debug)
  // //Serial.print("Subscribed to the topic ");
  // //Serial.println(Topic);
}

void setup() {

  pinMode(A4, INPUT);
  pinMode(A5, INPUT);

  //Serial.begin(115200);
  WiFi.setPins(4, 8, 12);
  delay(1000);

  ConnectWiFi();
}

void loop() {

  // Speed and turn value
  Speed();
  Turn();

  // Checking for change
  if (speed_val != prev_speed_val) {

    if (speed_val == 0) {

      // Stopping speed
      sendDataValue[2] = 0;

      // Publish
      client.publish("vroom", sendDataValue, 8);

      /*if (turn_val < 0) {

        // Resending turn speed
        sendDataValue[2] = 3;
        sendDataValue[6] = abs(turn_val);

        // Publish
        client.publish(Topic, sendDataValue, 8);
      }
      else if (turn_val > 0) {

        // Resending turn speed
        sendDataValue[2] = 4;
        sendDataValue[6] = turn_val;

        // Publish
        client.publish(Topic, sendDataValue, 8);
      }*/
    }
    if (speed_val < 0) {

      // Set action to back and set pos speed
      sendDataValue[2] = 2;
      sendDataValue[6] = abs(speed_val);

      // Publish
      client.publish("vroom", sendDataValue, 8);
    }
    else if (speed_val > 0) {

      // Set action to forward and set speed
      sendDataValue[2] = 1;
      sendDataValue[6] = speed_val;

      // Publish
      client.publish("vroom", sendDataValue, 8);
    }

    // Saving the speed value
    prev_speed_val = speed_val;
  }

  // Checking for change
  if (turn_val != prev_turn_val) {

    if (turn_val == 0) {

        sendDataValue[2] = 5;

        // Publish
        client.publish("vroom", sendDataValue, 8);
        
      /*if (prev_turn_val < 0) {

        // Setting function left stop
        sendDataValue[2] = 5;

        // Publish
        client.publish(Topic, sendDataValue, 8);
      }
      else if (prev_turn_val > 0) {

        // Setting function right stop
        sendDataValue[2] = 6;

        // Publish
        client.publish(Topic, sendDataValue, 8);
      }*/

    }
    if (turn_val < 0) {

      // Set function left and turn speed
      sendDataValue[2] = 3;
      sendDataValue[6] = abs(turn_val);

      // Publish
      client.publish("vroom", sendDataValue, 8);
    }
    else if (turn_val > 0) {

      // Set function right and turn speed
      sendDataValue[2] = 4;
      sendDataValue[6] = turn_val;

      // Publish
      client.publish("vroom", sendDataValue, 8);
    }

    // Saving the turn value
    prev_turn_val = turn_val;
  }
}

void Speed(){

  /* Speed
   * This part will check if there is any change in the analog stick.
   * The deadzone of 50 is implemented so that the code can rest.
   * And don't have a constant change.
   * 
   * -204/204/-102/102/-51/51 are disabled.
   * This is to have enough space on the leonardo.
   * If you use a mega you can enable them.
   */

  // Analog value
  int val = analogRead(A4);

  //to Speed -255
  if (val < 50 && val < analog_Y_val && analog_Y_val != 50) {
    //Serial.println("Speed: -255");
    analog_Y_val = 50;
    speed_val = -255;
  }

  //to Speed -204
  /*else if (val < 150 && val < analog_Y_val && analog_Y_val != 100 && val > 50) {
    //Serial.println("Speed: -204");
    analog_Y_val = 100;
    speed_val = -204;
  }
  else if (val > 100 && val > analog_Y_val && val < 200 && analog_Y_val != 100) {
    //Serial.println("Speed: -204");
    analog_Y_val = 100;
    speed_val = -204;
  }

  //to Speed -153
  else if (val < 250 && val < analog_Y_val && analog_Y_val != 200 && val > 100) {
    //Serial.println("Speed: -153");
    analog_Y_val = 200;
    speed_val = -153;
  }
  else if (val > 200 && val > analog_Y_val && val < 300 && analog_Y_val != 200) {
    //Serial.println("Speed: -153");
    analog_Y_val = 200;
    speed_val = -153;
  }

  //to Speed -102
  else if (val < 350 && val < analog_Y_val && analog_Y_val != 300 && val > 200) {
    //Serial.println("Speed: -102");
    analog_Y_val = 300;
    speed_val = -102;
  }
  else if (val > 300 && val > analog_Y_val && val < 400 && analog_Y_val != 300) {
    //Serial.println("Speed: -102");
    analog_Y_val = 300;
    speed_val = -102;
  }

  //to Speed -51
  else if (val < 450 && val < analog_Y_val && analog_Y_val != 400 && val > 300) {
    //Serial.println("Speed: -51");
    analog_Y_val = 400;
    speed_val = -51;
  }
  else if (val > 400 && val > analog_Y_val && val < 500 && analog_Y_val != 400) {
    //Serial.println("Speed: -51");
    analog_Y_val = 400;
    speed_val = -51;
  }*/

  //to Speed 0
  else if (val < 550 && val < analog_Y_val && analog_Y_val != 500 && val > 400) {
    //Serial.println("Speed: 0");
    analog_Y_val = 500;
    speed_val = 0;
  }
  else if (val > 500 && val > analog_Y_val && val < 600 && analog_Y_val != 500) {
    //Serial.println("Speed: 0");
    analog_Y_val = 500;
    speed_val = 0;
  }

  //to Speed 51
  /*else if (val < 650 && val < analog_Y_val && analog_Y_val != 600 && val > 500) {
    //Serial.println("Speed: 51");
    analog_Y_val = 600;
    speed_val = 51;
  }
  else if (val > 600 && val > analog_Y_val && val < 700 && analog_Y_val != 600) {
    //Serial.println("Speed: 51");
    analog_Y_val = 600;
    speed_val = 51;
  }

  //to Speed 102
  else if (val < 750 && val < analog_Y_val && analog_Y_val != 700 && val > 600) {
    //Serial.println("Speed: 102");
    analog_Y_val = 700;
    speed_val = 102;
  }
  else if (val > 700 && val > analog_Y_val && val < 800 && analog_Y_val != 700) {
    //Serial.println("Speed: 102");
    analog_Y_val = 700;
    speed_val = 102;
  }

  //to Speed 153
  else if (val < 850 && val < analog_Y_val && analog_Y_val != 800 && val > 700) {
    //Serial.println("Speed: 153");
    analog_Y_val = 800;
    speed_val = 153;
  }
  else if (val > 800 && val > analog_Y_val && val < 900 && analog_Y_val != 800) {
    //Serial.println("Speed: 153");
    analog_Y_val = 800;
    speed_val = 153;
  }

  //to Speed 204
  else if (val < 950 && val < analog_Y_val && analog_Y_val != 900 && val > 800) {
    //Serial.println("Speed: 204");
    analog_Y_val = 900;
    speed_val = 204;
  }
  else if (val > 900 && val > analog_Y_val && val < 1000 && analog_Y_val != 900) {
    //Serial.println("Speed: 204");
    analog_Y_val = 900;
    speed_val = 204;
  }*/

  //to Speed 255
  else if (val > 1000 && val > analog_Y_val && analog_Y_val != 1000) {
    //Serial.println("Speed: 255");
    analog_Y_val = 1000;
    speed_val = 255;
  }
}

void Turn(){

  /* Turn
   * This part will check if there is any change in the analog stick.
   * The deadzone of 50 is implemented so that the code can rest.
   * And don't have a constant change.
   * 
   * -204/204/-102/102/-51/51 are disabled.
   * This is to have enough space on the leonardo.
   * If you use a mega you can enable them.
   */
  
  // Analog value
  int val = analogRead(A5);

  //to left -255
  if (val < 50 && val < analog_X_val && analog_X_val != 50) {
    //Serial.println("left: -255");
    analog_X_val = 50;
    turn_val = -255;
  }

  //to left -204
  /*else if (val < 150 && val < analog_X_val && analog_X_val != 100 && val > 50) {
    //Serial.println("left: -204");
    analog_X_val = 100;
    turn_val = -204;
  }
  else if (val > 100 && val > analog_X_val && val < 200 && analog_X_val != 100) {
    //Serial.println("left: -204");
    analog_X_val = 100;
    turn_val = -204;
  }

  //to left -153
  else if (val < 250 && val < analog_X_val && analog_X_val != 200 && val > 100) {
    //Serial.println("left: -153");
    analog_X_val = 200;
    turn_val = -153;
  }
  else if (val > 200 && val > analog_X_val && val < 300 && analog_X_val != 200) {
    //Serial.println("left: -153");
    analog_X_val = 200;
    turn_val = -153;
  }

  //to left -102
  else if (val < 350 && val < analog_X_val && analog_X_val != 300 && val > 200) {
    //Serial.println("left: -102");
    analog_X_val = 300;
    turn_val = -102;
  }
  else if (val > 300 && val > analog_X_val && val < 400 && analog_X_val != 300) {
    //Serial.println("left: -102");
    analog_X_val = 300;
    turn_val = -102;
  }

  //to left -51
  else if (val < 450 && val < analog_X_val && analog_X_val != 400 && val > 300) {
    //Serial.println("left: -51");
    analog_X_val = 400;
    turn_val = -51;
  }
  else if (val > 400 && val > analog_X_val && val < 500 && analog_X_val != 400) {
    //Serial.println("left: -51");
    analog_X_val = 400;
    turn_val = -51;
  }*/

  //to left/right 0
  else if (val < 550 && val < analog_X_val && analog_X_val != 500 && val > 400) {
    //Serial.println("left/right: 0");
    analog_X_val = 500;
    turn_val = 0;
  }
  else if (val > 500 && val > analog_X_val && val < 600 && analog_X_val != 500) {
    //Serial.println("left/right: 0");
    analog_X_val = 500;
    turn_val = 0;
  }

  //to right 51
  /*else if (val < 650 && val < analog_X_val && analog_X_val != 600 && val > 500) {
    //Serial.println("right: 51");
    analog_X_val = 600;
    turn_val = 51;
  }
  else if (val > 600 && val > analog_X_val && val < 700 && analog_X_val != 600) {
    //Serial.println("right: 51");
    analog_X_val = 600;
    turn_val = 51;
  }

  //to right 102
  else if (val < 750 && val < analog_X_val && analog_X_val != 700 && val > 600) {
    //Serial.println("right: 102");
    analog_X_val = 700;
    turn_val = 102;
  }
  else if (val > 700 && val > analog_X_val && val < 800 && analog_X_val != 700) {
    //Serial.println("right: 102");
    analog_X_val = 700;
    turn_val = 102;
  }

  //to right 153
  else if (val < 850 && val < analog_X_val && analog_X_val != 800 && val > 700) {
    //Serial.println("right: 153");
    analog_X_val = 800;
    turn_val = 153;
  }
  else if (val > 800 && val > analog_X_val && val < 900 && analog_X_val != 800) {
    //Serial.println("right: 153");
    analog_X_val = 800;
    turn_val = 153;
  }

  //to right 204
  else if (val < 950 && val < analog_X_val && analog_X_val != 900 && val > 800) {
    //Serial.println("right: 204");
    analog_X_val = 900;
    turn_val = 204;
  }
  else if (val > 900 && val > analog_X_val && val < 1000 && analog_X_val != 900) {
    //Serial.println("right: 204");
    analog_X_val = 900;
    turn_val = 204;
  }*/

  //to right 255
  else if (val > 1000 && val > analog_X_val && analog_X_val != 1000) {
    //Serial.println("right: 255");
    analog_X_val = 1000;
    turn_val = 255;
  }
}

