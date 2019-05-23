//including some libraries
#include <EEPROM.h>
#include "SerialCommand.h"
#include "EEPROMAnything.h"

//Defining the serialport, serial1 is the tx and rx on the atmega32u4
#define SerialPort Serial1

//setting the serialport in the library
SerialCommand sCmd(SerialPort);

//settings for the communication
#define Baudrate 115200
#define SERIALCOMMANDDEBUG 1

//settings for the light LED's
//from left to right: D11 --> digital pin 6 / D12 --> digital pin 12 / D9 --> digitalpin 3 / D10 --> digital pin 4
byte LEDIX = 3;
byte LEDX = 4;
byte LEDXI = 6;
byte LEDXII = 12;

//settings for left motor
int PWMA = 10; //plan B = 13 en plan A = 10
byte AIN1 = 8; //plan B = 11 en plan A = 8
byte AIN2 = 9; //plan B = 12 en plan A = 9

//Settings for right motor
int PWMB = 11; //plan B = 10 en plan A = 11
byte BIN1 = 5; //plan B = 9 en plan A = 5
byte BIN2 = 13; //plan B = 8 en plan A = 13

//standby of the TB6612fng
//byte STBY = 7;
//settings for the speed of the motors
int SpeedLeft = 0;
int SpeedRight = 0;

//setting the start/stop button on pin 2 and a bool for the startup
byte startButton = 2;

//make an array where all sensors are set, the sequence of the analog pins are important follow your print
const int channel[] = {A0, A1, A2, A3, A4, A5};

//start is true or false
bool start;

//the are the values that will be saved in the EEPROM
struct param_t
{
  byte speedPWM;
  float kp;
  float ki;
  float kd;
  int white[6];
  int black[6];  
  unsigned long cycleTime;
} params;

//these are to calculate the possition of the line under the linefollower
int value[6];
int normalised[6];

//variables for the PID
float error = 0;
float prevError = 0;
float average;
float errSum;
float output = 0;

//Output of the various PID controller components
float Pterm = 0;
float Iterm = 0;
float Dterm = 0;

//for use of an real time system
unsigned long time, prevTime, delta, calculationTime;


void setup() {
  //making an interrupt to start or stop the linefollower
  attachInterrupt(digitalPinToInterrupt(startButton), onStartup, FALLING);

  //PinMode for the two motors
  pinMode(PWMA, OUTPUT);
  pinMode(PWMB, OUTPUT);
  pinMode(AIN1, OUTPUT);
  pinMode(AIN2, OUTPUT);
  pinMode(BIN1, OUTPUT);
  pinMode(BIN2, OUTPUT);
  
  digitalWrite(7, HIGH);

  //PinMode for the LED's
  pinMode(LEDIX, OUTPUT);
  pinMode(LEDX, OUTPUT);
  pinMode(LEDXI, OUTPUT);
  pinMode(LEDXII, OUTPUT);

  //starting the serial port
  SerialPort.begin(Baudrate);

  //setting the possible commands for serial communication
  sCmd.addCommand("start", onStart);
  sCmd.addCommand("stop", onStop);
  sCmd.addCommand("set", onSet);
  sCmd.addCommand("debug", onDebug);
  sCmd.addCommand("reset", onReset);
  sCmd.addCommand("PID", onPID);
  sCmd.addCommand("WriteToEEPROM", onWriteToEEPROM);
  sCmd.addCommand("Calibrate", onCalibrate);
  sCmd.addCommand("getEEPROM", onGetEEPROM);
  //sCmd.addCommand("ManBest", onManBest);
  sCmd.addCommand("Status", onStatus);
  sCmd.addCommand("LED", onLED);
  sCmd.addCommand("zero", onZero);
  sCmd.setDefaultHandler(onUnknownCommand);

  //start reading anything that comes into the serial port
  EEPROM_readAnything(0, params);

  //setting start to false else the linefollower will start driving
  start = false;

  //for the use of the real time system setting the time values
  time = micros();
  prevTime = time;

  //print out that the linefollower is ready
  SerialPort.println("ready");
}

void loop() {
  
  //Reading all incomming serial data
  sCmd.readSerial();

  //setting the time to micros
  time = micros();

  //if the time is greater than the previous then calculate delta normal else it's calculated in a differant way (overflow)
  if (time > prevTime) {
    delta = time - prevTime;
  }
  else{
    delta = 4294967295 - prevTime + time + 1;
  }

  //if the delta is greater than the set cycletime then do what is under it
  if (delta > params.cycleTime)
  {
    //setting the precTime to time now
    prevTime = time;
      
    // Program in real time
    //when start is active
    if (start){

      //reading out all the sensors
      for (byte i = 0; i < 6; i++){
      value[i] = analogRead(channel[i]);
      }

      //comparing the values read by the saved values en setting them in a %
      for (byte i = 0; i < 6; i++){
        normalised[i] = map(value[i], params.black[i], params.white[i], 100, 0);
      }

      //calculating the weighted average
      average = (
                  (-225 * normalised[5]) +
                  (-135 * normalised[4]) +
                  (-45 * normalised[3]) +
                  (45 * normalised[2]) +
                  (134 * normalised[1]) +
                  (225 * normalised[0])
                );
      average /= (
                   normalised[5] +
                   normalised[4] +
                   normalised[3] +
                   normalised[2] +
                   normalised[1] +
                   normalised[0]
                 );

      //for testing with only a P value
      // double error = 0 - (double) average;
      // double output = params.kp * error;

      //saving the last error for use in the Dterm
      prevError = error;

      //calculating the error (0 is the setpoint on my linefollower it is in the middle of the car so 0
      error = 0 - average;

      //P of the PID
      Pterm = error * params.kp;

      //I of the PID
      Iterm += error * (params.cycleTime / 1000.0);

      //Iterm ceiling
      if (Iterm > 255){
        Iterm = 255;
      }
      if (Iterm < -255){
        Iterm = -255;
      }

      //D of the PID
      Dterm = (error - prevError) * params.kd;

      //Full PID
      output = Pterm + (Iterm * params.ki) + Dterm;

      //making sure the output value doesn't go over (under) 255 (-255)
      if(output > 255){
        output = 255;
      }
      else if(output < -255){
        output = -255;
      }

      //calculating the left and right speed
      SpeedLeft = params.speedPWM - output;
      SpeedRight = params.speedPWM + output;

      //PWM values can't be greater than the set PWM (max) or smaller than -set PWM (min)
      if (SpeedLeft > params.speedPWM) SpeedLeft = params.speedPWM;
      if (SpeedLeft < -params.speedPWM) SpeedLeft = -params.speedPWM;

      if (SpeedRight > params.speedPWM) SpeedRight = params.speedPWM;
      if (SpeedRight < -params.speedPWM) SpeedRight = -params.speedPWM;

      //checking if the motors need to turn back or forward
      if (SpeedLeft > 0) {
        digitalWrite(AIN1, LOW);
        digitalWrite(AIN2, HIGH);
      }
      else {
        digitalWrite(AIN1, HIGH);
        digitalWrite(AIN2, LOW);
      }

      if (SpeedRight > 0) {
        digitalWrite(BIN1, HIGH);
        digitalWrite(BIN2, LOW);
      }
      else {
        digitalWrite(BIN1, LOW);
        digitalWrite(BIN2, HIGH);
      }

      //Writing the analog values to  the motors (need to be absolute)
      analogWrite(PWMA, abs(SpeedLeft));
      analogWrite(PWMB, abs(SpeedRight));

    }

    else{

      //if start = false putting no PWM on the motors
      digitalWrite(PWMA, 0);
      digitalWrite(PWMB, 0);
    
    }
  }

  //Calculating the perfect time for the cyclus
  unsigned long difference = micros() - time;
  if (difference > calculationTime) calculationTime = difference; 
 
}

void onUnknownCommand(char *command)
{
  SerialPort.print("The command you entered is unknown: \"");
  SerialPort.print(command);
  SerialPort.println("\"");
}

void onSet()
{
  char* parameter = sCmd.next();
  char* value = sCmd.next();

  //setting speed
  if (value == ""){

    SerialPort.println("set <parameter> <value>");

  }
  else{

    if (strcmp(parameter, "speed") == 0) {
    
    params.speedPWM = atoi(value);
    SerialPort.print("Speed set to: ");
    SerialPort.println(params.speedPWM);
    }

 
    //setting cycleTime
    else if (strcmp(parameter, "cycleTime") == 0){
    
      params.cycleTime = atol(value);
      SerialPort.print("cycleTime set to: ");
      SerialPort.println(params.cycleTime);
    }

    else{
      SerialPort.println("set <parameter> <value>");
    }    
  }
}

void onPID()
{
  
   //setting kp value
  char* valueKp = sCmd.next();
  char* valueKi = sCmd.next();
  char* valueKd = sCmd.next();
  
  if (valueKp == "" or valueKi == "" or valueKd == ""){
    
    SerialPort.println("PID <valueKp> <valueKi> <valueKd>");
  }
  
  else {
  
    params.kp = atof(valueKp);
    params.ki = atof(valueKi);
    params.kd = atof(valueKd);

    SerialPort.print("PID has been set to a Kp value of ");
    SerialPort.print(params.kp);
    SerialPort.print(" a Ki value of ");
    SerialPort.print(params.ki);
    SerialPort.print(" and a Kd value of ");
    SerialPort.print(params.kd);
    SerialPort.println(".");
    SerialPort.println("");
  }
}

void onWriteToEEPROM()
{
  EEPROM_writeAnything(0, params);
  SerialPort.println("Saved");
}

void onStart()
{
  start = HIGH;
  SerialPort.println("Start");
  SerialPort.println(start);
}

void onStop()
{
  start = LOW;
  SerialPort.println("Stop");
  SerialPort.println(start);
}

void onStartup()
{
  
  start = not start;
 
}

void onDebug()
{
  SerialPort.print("speed: ");
  SerialPort.println(params.speedPWM);
  SerialPort.print("kp: ");
  SerialPort.println(params.kp); 
  SerialPort.print("running: ");
  SerialPort.println(start);
  SerialPort.println(calculationTime);

  //analog values
  SerialPort.print("Sensor values: ");
  for (int i = 0; i < 6; i++){
    SerialPort.print(value[i]);
    SerialPort.print(" ");
  }
  SerialPort.println();

  //calibrate white values
  SerialPort.print("Calibrate white values: ");
  for (int i = 0; i < 6; i++){
    SerialPort.print(params.white[i]);
    SerialPort.print(" ");
  }
  SerialPort.println();

  //calibrate black values
  SerialPort.print("Calibrate black values: ");
  for (int i = 0; i < 6; i++){
    SerialPort.print(params.black[i]);
    SerialPort.print(" ");
  }
  SerialPort.println();

  //normilased values
  SerialPort.print("Normilased values: ");
  for (int i = 0; i < 6; i++){
    SerialPort.print(normalised[i]);
    SerialPort.print(" ");
  }
  SerialPort.println();

  SerialPort.print("Position: ");
  SerialPort.println(average);
  
}

void onStatus()
{
  //send status of a few things to the controll system
  // running, speed (PWM), Linefollower by, Cycletime clac and set
  SerialPort.println("<status>");
  SerialPort.println(start);
  SerialPort.println(params.speedPWM);
  SerialPort.println("Linefollower by Sarrazyn J.");
  SerialPort.println(params.cycleTime);
  SerialPort.println(calculationTime);
  SerialPort.println(params.kp);
  SerialPort.println(params.ki);
  SerialPort.println(params.kd);
  SerialPort.print("<done>");
}

void onReset()
{
  SerialPort.print("resetting parameters... ");
  EEPROM_resetAnything(0, params);
  EEPROM_readAnything(0, params);  
  SerialPort.println("done");
}
 
void onGetEEPROM()
{
  SerialPort.println("**********************************************************************************");
  SerialPort.println("The saved values of this linefollower are:");
  SerialPort.print("Speed: ");
  SerialPort.println(params.speedPWM);
  SerialPort.println("PID:");
  SerialPort.print("      -Kp: ");
  SerialPort.println(params.kp);
  SerialPort.print("      -Ki: ");
  SerialPort.println(params.ki);
  SerialPort.print("      -Kd: ");
  SerialPort.println(params.kd);
  SerialPort.print("CycleTime: ");
  SerialPort.println(params.cycleTime);
  SerialPort.println("**********************************************************************************");
}

void onCalibrate()
{
  char* arg = sCmd.next();

  if (strcmp(arg, "white") == 0){
    for (int i = 0; i < 6; i++) {params.white[i] = analogRead (channel[i]);}
    SerialPort.println("Calibrated white values");
  }
  else if (strcmp(arg, "black") == 0){
    for (int i = 0; i < 6; i++) {params.black[i] = analogRead (channel[i]);}
    SerialPort.println("Calibrated black values");
  }
  else {
    SerialPort.println("calibrate <arg>");
  }
}

/*void onManBest()
{
  char* arg = sCmd.next();

  if (strcmp(arg, "Stop") == 0){

    SpeedLeft = 0;
    SpeedRight = 0;
    
  }
  
  else if (strcmp(arg, "Forward") == 0){

    digitalWrite(AIN1, LOW);
    digitalWrite(AIN2, HIGH);
    digitalWrite(BIN1, LOW);
    digitalWrite(BIN2, HIGH);
    SpeedLeft = 150;
    SpeedRight = 150;
    
  }

  else if (strcmp(arg, "Back") == 0){

    digitalWrite(AIN1, HIGH);
    digitalWrite(AIN2, LOW);
    digitalWrite(BIN1, HIGH);
    digitalWrite(BIN2, LOW);
    SpeedLeft = 96;
    SpeedRight = 96;
    
  }

  else if (strcmp(arg, "Left") == 0){

    if (SpeedLeft == SpeedRight){
        
        SpeedRight = SpeedRight - 60;
      }
  }

  else if (strcmp(arg, "LeftNormal") == 0){

    SpeedRight = SpeedLeft;
  }

  else if (strcmp(arg, "Right") == 0){

    if (SpeedRight == SpeedLeft){
        
        SpeedLeft = SpeedLeft- 60;
        
      }
  }

  else if (strcmp(arg, "RightNormal") == 0){

    SpeedLeft = SpeedRight;
  }
  
  else if (strcmp(arg, "Boost") == 0){

    SpeedLeft = 255;
    SpeedRight = 255;
  }

  else if (strcmp(arg, "Roll") == 0){

    SpeedLeft = 70;
    SpeedRight = 70;
  }

  else {
    SerialPort.println("ManBest <arg>");
  }
}*/

void onLED()
{
  char* onOF = sCmd.next();
  char* arg = sCmd.next();
    
  //from left to right: LEDXI LEDXII LEDIX LEDX
  if (strcmp(onOF, "on") == 0){
    
    if (strcmp(arg, "XI") == 0){
    
      digitalWrite(LEDXI, HIGH);
      
    }
    if (strcmp(arg, "XII") == 0){
    
      digitalWrite(LEDXII, HIGH);
      
    }
    if (strcmp(arg, "IX") == 0){
    
      digitalWrite(LEDIX, HIGH);
      
    }
    if (strcmp(arg, "X") == 0){
    
      digitalWrite(LEDX, HIGH);
      
    }
  }

  if (strcmp(onOF, "off") == 0){

    if (strcmp(arg, "XI") == 0){
    
      digitalWrite(LEDXI, LOW);
      
    }
    if (strcmp(arg, "XII") == 0){
    
      digitalWrite(LEDXII, LOW);
      
    }
    if (strcmp(arg, "IX") == 0){
    
      digitalWrite(LEDIX, LOW);
      
    }
    if (strcmp(arg, "X") == 0){
    
      digitalWrite(LEDX, LOW);
      
    }
    
  }
 
}

void onZero()
{
  
}

/*
void Drive (byte speedL, byte speedR){

  leftMotor(speedL);
  rightMotor(speedR);
  
}

void leftMotor(byte speedL){

  //setMotorDir(1, dir);
  analogWrite(PWMA, speedL);
}

void rightMotor(byte speedR){

  //setMotorDir(2, dir);
  analogWrite(PWMB, speedR);
}

void setMotorDir(byte motor, bool dir){

  switch (motor){

    case 1:
      digitalWrite(AIN1, !dir);
      digitalWrite(AIN2, dir);
      break;

    case 2:
      digitalWrite(BIN1, dir);
      digitalWrite(BIN2, !dir);
      break;
  }
}
*/
