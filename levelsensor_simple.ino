#include <LiquidCrystal.h>

int pulsePin = 12;
int capPin = 13;

float pulseTime;
bool pulseIsHigh = false;
bool capIsHigh = false;
const int N_SAMPLES = 500;
const bool EXT_REF = false;
const unsigned int INT_REF_FREQ = 200; // Hz
const float CALIBRATION_SLOPE = 6.1; // us/cm
const float CALIBRATION_INTERCEPT = 288; // us
int currentSample = 0;
float averageTime = 0;

LiquidCrystal lcd(2, 3, 4, 5, 6, 7);

void setup() {
  Serial.begin(9600);
  lcd.begin(16, 2);
  lcd.print("Starting up...");
  if( !EXT_REF ) {
    pinMode(pulsePin, OUTPUT);
    tone(pulsePin, INT_REF_FREQ);
  } else {
    pinMode(pulsePin, INPUT);
  }
  pinMode(capPin, INPUT);
}

void read_level_once() {
  while(true) {
    if (!pulseIsHigh && !capIsHigh) {
      // Wait for pulse to go high
      int pulseVal = digitalRead(pulsePin);
      if (pulseVal == HIGH) {
        pulseTime = float(micros());
        pulseIsHigh = true;
      }
    }
    if (pulseIsHigh && !capIsHigh) {
      // Wait for cap to go high
      int capVal = digitalRead(capPin);
      if (capVal == HIGH) {
        capIsHigh = true;
        // Add to average
        if (currentSample < N_SAMPLES) {
          averageTime = averageTime + (micros() - pulseTime) / N_SAMPLES;
          currentSample = currentSample + 1;
        }
        if (currentSample == N_SAMPLES) {
          // Reset
          currentSample = 0;
          Serial.println(averageTime);
          lcd.clear();
          lcd.setCursor(0, 0);
          lcd.print(averageTime);
          lcd.print(" ");
          lcd.print(char(B11100100));
          lcd.print("s");
          lcd.setCursor(0, 1);
          lcd.print((averageTime - CALIBRATION_INTERCEPT) / CALIBRATION_SLOPE);
          lcd.print(" cm");
          averageTime = 0;
          return;
        }
      }
    }
    if (pulseIsHigh && capIsHigh) {
      // Wait for pulse to go low
      int pulseVal = digitalRead(pulsePin);
      if (pulseVal == LOW) {
        pulseIsHigh = false;
      }
    }
    if (!pulseIsHigh && capIsHigh) {
      // Wait for cap to go low
      int capVal = digitalRead(capPin);
      if (capVal == LOW) {
        capIsHigh = false;
      } 
    } 
  }
}

void loop() {
  read_level_once();
  Serial.flush();
}
