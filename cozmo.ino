#include <MX1508.h>

#define RIGHTPINA 9
#define RIGHTPINB 10
#define NUMPWM 2
#define PWM 100
#define LEFTPINA 5
#define LEFTPINB 6

MX1508 motorA(RIGHTPINA,RIGHTPINB, FAST_DECAY, NUMPWM);
MX1508 motorB(LEFTPINA,LEFTPINB, FAST_DECAY, NUMPWM);

byte cx = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(13,OUTPUT);
  digitalWrite(13,HIGH);
  delay(3000);
  digitalWrite(13,LOW);
}

void GoForward(){
  motorA.motorGo(PWM);
  motorB.motorGo(200);
}
void GoLeft(){
  motorA.motorGo(-700);
  motorB.motorGo(750);
}
void GoRight(){
  motorA.motorGo(700);
  motorB.motorGo(-750);
}
void stop(){
  motorA.stopMotor();
  motorB.stopMotor();
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()!=0){
    cx = Serial.read();
    if(cx>128){
      GoRight();
      delay(10);
    }
    else if(cx<126 and cx >0){
      GoLeft();
      delay(10);
    }
    else if(cx == 127){
      GoForward();
      delay(10);
    }
    else if(cx == 0){
      stop();
      delay(10);
    }
  }
  
}






