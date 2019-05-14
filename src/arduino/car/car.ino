#include <WiFi101.h>
#include <PubSubClient.h>

WiFiClient ClientMega;
PubSubClient client(ClientMega);

const char* ssid = "StageSupernet";
const char* password = "StageSupernet";
int status = WL_IDLE_STATUS;

const char* Topic = "vroom";
byte thisCar = 20;

char* mqttServer = "192.168.1.5";
int mqttPort = 1881;

byte MessageByte[9];
byte prevMessageByte = 9;

byte currentSpeed = 0;
byte PWMleft = 44;
byte left2 = 40;
byte left1 = 41;
byte STBY = 47;
byte right1 = 43;
byte right2 = 42;
byte PWMright = 46;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  WiFi.setPins(22, 23, 24);
  delay(1000);

  digitalWrite(STBY, HIGH);
  
  ConnectWiFi();
}

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

    if (client.connect(thisCar)) {
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

void loop() {

  client.loop();

  /* for debugging

      for (int i = 0; i<9; i++){
        Serial.print(byte(MessageByte[i]), BIN);
        Serial.print("//");
      }
      Serial.println();
      Serial.println("-----------------------");
  */
  if (MessageByte[2] != prevMessageByte) {

    prevMessageByte = MessageByte[2];

    if (MessageByte[0] == thisCar) {
      if (MessageByte[2] == 0) {
        
        currentSpeed = 0;
        Stop();
        Serial.println("Stop");
      }
      else if (MessageByte[2] == 1) {

        currentSpeed = MessageByte[6];
        Forward(currentSpeed);
        Serial.println("Forward");
      }
      else if (MessageByte[2] == 2) {

        currentSpeed = MessageByte[6];
        Back(currentSpeed);
        Serial.println("Back");
      }
      else if (MessageByte[2] == 3) {

        Left(MessageByte[6]);
        Serial.println("Left");
      }
      else if (MessageByte[2] == 4) {

        Right(MessageByte[6]);
        Serial.println("Right");
      }
      else if (MessageByte[2] == 5) {

        setPWM(currentSpeed, currentSpeed);
        Serial.println("Left stop");
      }
      else if (MessageByte[2] == 6) {

        setPWM(currentSpeed, currentSpeed);
        Serial.println("Right stop");
      }
    }
  }
}

void Stop(){

  setPWM(0, 0);
}

void Forward(byte PWM){
  
  digitalWrite(left1, HIGH);
  digitalWrite(left2, LOW);
  digitalWrite(right1, HIGH);
  digitalWrite(right2, LOW);
  setPWM(PWM, PWM);
}

void Back(byte PWM){

  digitalWrite(left1, LOW);
  digitalWrite(left2, HIGH);
  digitalWrite(right1, LOW);
  digitalWrite(right2, HIGH);
  setPWM(PWM, PWM);
}

void Left(byte PWM){

  int turnSpeed;

  turnSpeed = currentSpeed - PWM;

  if (turnSpeed < 0){
    
    digitalWrite(right1, HIGH);
    digitalWrite(right2, LOW);
    setPWM(0, PWM);
  }
  else {

    setPWM(turnSpeed, currentSpeed);
  }
}

void Right(byte PWM){

  int turnSpeed;

  turnSpeed = currentSpeed - PWM;

  if (turnSpeed < 0){
    
    digitalWrite(left1, HIGH);
    digitalWrite(left2, LOW);
    setPWM(PWM, 0);
  }
  else {

    setPWM(currentSpeed, turnSpeed);
  }
}

void setPWM(byte PWMLeft, byte PWMRight){

  analogWrite(PWMleft, PWMLeft);
  analogWrite(PWMright, PWMRight);
  Serial.println(PWMLeft);
  Serial.println(PWMRight);
}


