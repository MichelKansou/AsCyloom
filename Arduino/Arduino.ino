#include <Wire.h>

#define SLAVE_ADRESS 0x12

int dataReceived = 0;
int dataSend = 0;

int speed = 250;

int magnet = 6;

int L1 = 5;

int motor1_enablePin = 11; 
int motor1_in1Pin = 13;
int motor1_in2Pin = 12;
 
int motor2_enablePin = 10; 
int motor2_in1Pin = 8;
int motor2_in2Pin = 7;

const byte TRIGGER_PIN = 2; // Broche TRIGGER
const byte ECHO_PIN = 3;    // Broche ECHO
/* Constantes pour le timeout */
const unsigned long MEASURE_TIMEOUT = 25000UL; // 25ms = ~8m à 340m/s
/* Vitesse du son dans l'air en mm/us */
const float SOUND_SPEED = 340.0 / 1000;

void setup(){
  initialize();
}

void loop(){
  //delay(100); // <- a voir si utile, c'est peut etre lui qui nique la detection d'obstacle
  scan();
}

void receiveData(int byteCount){
  while(Wire.available()){
    dataReceived = Wire.read();
    switch(dataReceived){
      
      /* 0 to 4 => direction */
      case 0: Stop(0); break;
      case 1: forward(speed); break;
      case 2: backward(speed); break;
      case 3: left(speed); break;
      case 4: right(speed); break;
      
      /* 5 to 6 => magnet */
      case 5: toggleMagnet(true); break;
      case 6: toggleMagnet(false); break;

      /* 7 to 10 => speed */
      case 7: speed = 175; break;
      case 8: speed = 200; break;
      case 9: speed = 230; break;
      case 10: speed = 255; break;

      /* 11 to 12 => LED */
      case 11: toggleLED(true); break;
      case 12: toggleLED(false); break;

      /* default */
      default: Stop(0); break;
      
    }
  }
}

void sendData(){
    Wire.write(dataSend);
}

void scan(){
  /* Starts calculation by sending a 10μs HIGH pulse on the TRIGGER pin */
  digitalWrite(TRIGGER_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGGER_PIN, LOW);

  /* Estimates the time between sending the ultrasonic pulse and its echo (if it exists) */
  long measure = pulseIn(ECHO_PIN, HIGH, MEASURE_TIMEOUT);

  /* Calculate the distance from the result */
  float distance_mm = measure / 2.0 * SOUND_SPEED;

 /* Serial.print(F("Distance: "));
  Serial.print(distance_mm);*/

  dataSend = (int)distance_mm;
  dataSend = dataSend / 10;
}

void Stop(int speed){
  setMotor1(speed, false);
  setMotor2(speed, false);
}

void forward(int speed){
  setMotor1(speed, false);
  setMotor2(speed, true);
}

void backward(int speed){
  setMotor1(speed, true);
  setMotor2(speed, false);
}

void left(int speed){
  setMotor1(speed, false);
  setMotor2(speed, false);
}

void right(int speed){
  setMotor1(speed, true);
  setMotor2(speed, true);
}

void setMotor1(int speed, boolean reverse)
{
  analogWrite(motor1_enablePin, speed);
  digitalWrite(motor1_in1Pin, ! reverse);
  digitalWrite(motor1_in2Pin, reverse);
}
 
void setMotor2(int speed, boolean reverse)
{
  analogWrite(motor2_enablePin, speed);
  digitalWrite(motor2_in1Pin, ! reverse);
  digitalWrite(motor2_in2Pin, reverse);
}

void toggleMagnet(boolean activate){
  if(activate){ 
    digitalWrite(magnet, HIGH);
  }
  else{
    digitalWrite(magnet, LOW); 
  }
}

void toggleLED(boolean activate){
    if(activate){ 
    digitalWrite(L1, HIGH);
  }
  else{
    digitalWrite(L1, LOW); 
  }
}

void initialize(){
  /* I2C */
  Serial.begin(9600);
  Wire.begin(SLAVE_ADRESS);
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);

 /* Motors */
  pinMode(motor1_in1Pin, OUTPUT);
  pinMode(motor1_in2Pin, OUTPUT);
  pinMode(motor1_enablePin, OUTPUT);
  pinMode(motor2_in1Pin, OUTPUT);
  pinMode(motor2_in2Pin, OUTPUT);
  pinMode(motor2_enablePin, OUTPUT);

  /* LED */
  pinMode(L1, OUTPUT); //L1 est une broche de sortie

  /* Magnet */
  pinMode(magnet, OUTPUT); 
  digitalWrite(magnet, LOW);  

  /* Echo-sounder */
  pinMode(TRIGGER_PIN, OUTPUT);
  digitalWrite(TRIGGER_PIN, LOW); // La broche TRIGGER doit être à LOW au repos
  pinMode(ECHO_PIN, INPUT);
}




