/* USB Joystick
 *
 * This program is used to read analog value and send it over the USB.
 * The python program usb_joystick.py is used to read the Serial communication.
 * That program will put the message on the mqtt.
 * 
 * Written by J. Sarrazyn
 */

// Name of the device
byte thisDevice = 23;

// Target device
byte target = 60;

byte dataType = 11;
byte Tail = 83;

// Message to send
byte dataValue[8] = {0, 0, 0, 0, 0, 0, 0, 0};

// Ports for the joystick
int Y_speed = A4;
int X_turn = A5;

// Speed and turn value
int speed_val;
int turn_val;

// Previous speed and turn value
int prev_speed_val;
int prev_turn_val;

// For checking the change
int analog_Y_val;
int analog_X_val;

void setup() {

  pinMode(Y_speed, INPUT);
  pinMode(X_turn, INPUT);

  Serial.begin(115200);

  delay(1000);

  dataValue[0] = target;
  dataValue[1] = thisDevice;
  dataValue[4] = dataType;
  dataValue[7] = Tail;
}

void loop() {

  // Speed and turn value
  Speed(Y_speed);
  Turn(X_turn);

  DataCheck();
}

void Speed(int port) {
  /* Speed
   *
   * This part will check if there is any change in the analog stick.
   * The deadzone of 50 is implemented so that the code can rest.
   * And don't have a constant change.
   */

  // Analog value
  int val = analogRead(port);

  //to Speed -255
  if (val < 50 && val < analog_Y_val && analog_Y_val != 50) {

    analog_Y_val = 50;
    speed_val = -255;
  }

  //to Speed -204
  else if (val < 150 && val < analog_Y_val && analog_Y_val != 100 && val > 50) {

    analog_Y_val = 100;
    speed_val = -204;
  }
  else if (val > 100 && val > analog_Y_val && val < 200 && analog_Y_val != 100) {

    analog_Y_val = 100;
    speed_val = -204;
  }

  //to Speed -153
  else if (val < 250 && val < analog_Y_val && analog_Y_val != 200 && val > 100) {

    analog_Y_val = 200;
    speed_val = -153;
  }
  else if (val > 200 && val > analog_Y_val && val < 300 && analog_Y_val != 200) {

    analog_Y_val = 200;
    speed_val = -153;
  }

  //to Speed -102
  else if (val < 350 && val < analog_Y_val && analog_Y_val != 300 && val > 200) {

    analog_Y_val = 300;
    speed_val = -102;
  }
  else if (val > 300 && val > analog_Y_val && val < 400 && analog_Y_val != 300) {

    analog_Y_val = 300;
    speed_val = -102;
  }

  //to Speed -51
  else if (val < 450 && val < analog_Y_val && analog_Y_val != 400 && val > 300) {

    analog_Y_val = 400;
    speed_val = -51;
  }
  else if (val > 400 && val > analog_Y_val && val < 500 && analog_Y_val != 400) {

    analog_Y_val = 400;
    speed_val = -51;
  }

  //to Speed 0
  else if (val < 550 && val < analog_Y_val && analog_Y_val != 500 && val > 400) {

    analog_Y_val = 500;
    speed_val = 0;
  }
  else if (val > 500 && val > analog_Y_val && val < 600 && analog_Y_val != 500) {

    analog_Y_val = 500;
    speed_val = 0;
  }

  //to Speed 51
  else if (val < 650 && val < analog_Y_val && analog_Y_val != 600 && val > 500) {

    analog_Y_val = 600;
    speed_val = 51;
  }
  else if (val > 600 && val > analog_Y_val && val < 700 && analog_Y_val != 600) {

    analog_Y_val = 600;
    speed_val = 51;
  }

  //to Speed 102
  else if (val < 750 && val < analog_Y_val && analog_Y_val != 700 && val > 600) {

    analog_Y_val = 700;
    speed_val = 102;
  }
  else if (val > 700 && val > analog_Y_val && val < 800 && analog_Y_val != 700) {

    analog_Y_val = 700;
    speed_val = 102;
  }

  //to Speed 153
  else if (val < 850 && val < analog_Y_val && analog_Y_val != 800 && val > 700) {

    analog_Y_val = 800;
    speed_val = 153;
  }
  else if (val > 800 && val > analog_Y_val && val < 900 && analog_Y_val != 800) {

    analog_Y_val = 800;
    speed_val = 153;
  }

  //to Speed 204
  else if (val < 950 && val < analog_Y_val && analog_Y_val != 900 && val > 800) {

    analog_Y_val = 900;
    speed_val = 204;
  }
  else if (val > 900 && val > analog_Y_val && val < 1000 && analog_Y_val != 900) {

    analog_Y_val = 900;
    speed_val = 204;
  }

  //to Speed 255
  else if (val > 1000 && val > analog_Y_val && analog_Y_val != 1000) {

    analog_Y_val = 1000;
    speed_val = 255;
  }
}

void Turn(int port) {
  /* Turn
   *
   * This part will check if there is any change in the analog stick.
   * The deadzone of 50 is implemented so that the code can rest.
   * And don't have a constant change.
   */

  // Analog value
  int val = analogRead(port);

  //to left -255
  if (val < 50 && val < analog_X_val && analog_X_val != 50) {

    analog_X_val = 50;
    turn_val = -255;
  }

  //to left -204
  else if (val < 150 && val < analog_X_val && analog_X_val != 100 && val > 50) {

    analog_X_val = 100;
    turn_val = -204;
  }
  else if (val > 100 && val > analog_X_val && val < 200 && analog_X_val != 100) {

    analog_X_val = 100;
    turn_val = -204;
  }

  //to left -153
  else if (val < 250 && val < analog_X_val && analog_X_val != 200 && val > 100) {

    analog_X_val = 200;
    turn_val = -153;
  }
  else if (val > 200 && val > analog_X_val && val < 300 && analog_X_val != 200) {

    analog_X_val = 200;
    turn_val = -153;
  }

  //to left -102
  else if (val < 350 && val < analog_X_val && analog_X_val != 300 && val > 200) {

    analog_X_val = 300;
    turn_val = -102;
  }
  else if (val > 300 && val > analog_X_val && val < 400 && analog_X_val != 300) {

    analog_X_val = 300;
    turn_val = -102;
  }

  //to left -51
  else if (val < 450 && val < analog_X_val && analog_X_val != 400 && val > 300) {

    analog_X_val = 400;
    turn_val = -51;
  }
  else if (val > 400 && val > analog_X_val && val < 500 && analog_X_val != 400) {

    analog_X_val = 400;
    turn_val = -51;
  }

  //to left/right 0
  else if (val < 550 && val < analog_X_val && analog_X_val != 500 && val > 400) {

    analog_X_val = 500;
    turn_val = 0;
  }
  else if (val > 500 && val > analog_X_val && val < 600 && analog_X_val != 500) {

    analog_X_val = 500;
    turn_val = 0;
  }

  //to right 51
  else if (val < 650 && val < analog_X_val && analog_X_val != 600 && val > 500) {

    analog_X_val = 600;
    turn_val = 51;
  }
  else if (val > 600 && val > analog_X_val && val < 700 && analog_X_val != 600) {

    analog_X_val = 600;
    turn_val = 51;
  }

  //to right 102
  else if (val < 750 && val < analog_X_val && analog_X_val != 700 && val > 600) {

    analog_X_val = 700;
    turn_val = 102;
  }
  else if (val > 700 && val > analog_X_val && val < 800 && analog_X_val != 700) {

    analog_X_val = 700;
    turn_val = 102;
  }

  //to right 153
  else if (val < 850 && val < analog_X_val && analog_X_val != 800 && val > 700) {

    analog_X_val = 800;
    turn_val = 153;
  }
  else if (val > 800 && val > analog_X_val && val < 900 && analog_X_val != 800) {

    analog_X_val = 800;
    turn_val = 153;
  }

  //to right 204
  else if (val < 950 && val < analog_X_val && analog_X_val != 900 && val > 800) {

    analog_X_val = 900;
    turn_val = 204;
  }
  else if (val > 900 && val > analog_X_val && val < 1000 && analog_X_val != 900) {

    analog_X_val = 900;
    turn_val = 204;
  }

  //to right 255
  else if (val > 1000 && val > analog_X_val && analog_X_val != 1000) {

    analog_X_val = 1000;
    turn_val = 255;
  }
}

void DataCheck() {

  // Checking for change
  if (speed_val != prev_speed_val) {

    if (speed_val == 0) {

      // Stopping speed
      dataValue[2] = 0;
      dataValue[6] = 0;

      // Send data over USB
      SendData();

      if (turn_val < 0) {

        // Resending turn speed
        dataValue[2] = 3;
        dataValue[6] = abs(turn_val);

        // Send data over USB
        SendData();
      }
      else if (turn_val > 0) {

        // Resending turn speed
        dataValue[2] = 4;
        dataValue[6] = turn_val;

        // Send data over USB
        SendData();
      }
    }
    if (speed_val < 0) {

      // Set action to back and set pos speed
      dataValue[2] = 2;
      dataValue[6] = abs(speed_val);

      // Send data over USB
      SendData();
    }
    else if (speed_val > 0) {

      // Set action to forward and set speed
      dataValue[2] = 1;
      dataValue[6] = speed_val;

      // Send data over USB
      SendData();
    }

    // Saving the speed value
    prev_speed_val = speed_val;
  }

  // Checking for change
  if (turn_val != prev_turn_val) {

    if (turn_val == 0) {

      if (prev_turn_val < 0) {

        // Setting function left stop
        dataValue[2] = 5;
        dataValue[6] = 0;

        // Send data over USB
        SendData();
      }
      else if (prev_turn_val > 0) {

        // Setting function right stop
        dataValue[2] = 6;
        dataValue[6] = 0;

        // Send data over USB
        SendData();
      }
    }
    if (turn_val < 0) {

      // Set function left and turn speed
      dataValue[2] = 3;
      dataValue[6] = abs(turn_val);

      // Send data over USB
      SendData();
    }
    else if (turn_val > 0) {

      // Set function right and turn speed
      dataValue[2] = 4;
      dataValue[6] = turn_val;

      // Send data over USB
      SendData();
    }

    // Saving the turn value
    prev_turn_val = turn_val;
  }
}

void SendData() {

  for (int i = 0; i < sizeof(dataValue); i++) {
    // Serial.write(dataValue[i]);
    Serial.print(dataValue[i]);
    Serial.print("//");
  }
  Serial.println("");
}

