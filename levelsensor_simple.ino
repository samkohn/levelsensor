#include <LiquidCrystal.h>

int pulsePin = 12;
int capPin = 13;

float pulseTime;
bool pulseIsHigh = false;
bool capIsHigh = false;
const int N_SAMPLES = 500;
const bool EXT_REF = false;
const unsigned int INT_REF_FREQ = 140; // Hz
const float CALIBRATION_SLOPE = 2.5; // us/cm
const float CALIBRATION_INTERCEPT = 321; // us
int currentSample = 0;
float averageTime = 0;
float averageSquaredTime = 0;

LiquidCrystal lcd(2, 3, 4, 5, 6, 7);
byte customChar[8] = {
  0b00100,
  0b00100,
  0b11111,
  0b00100,
  0b00100,
  0b00000,
  0b11111,
  0b00000
};
void setup() {
  Serial.begin(9600);
  lcd.createChar(0, customChar);
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
          float currentTime = micros() - pulseTime;
          averageTime = averageTime + currentTime / N_SAMPLES;
          averageSquaredTime = averageSquaredTime + currentTime*currentTime / N_SAMPLES;
          currentSample = currentSample + 1;
        }
        if (currentSample == N_SAMPLES) {
          // Reset
          currentSample = 0;
          float measurement = (averageTime - CALIBRATION_INTERCEPT)/CALIBRATION_SLOPE;
          float error_time = sqrt(averageSquaredTime - averageTime*averageTime);
          float error_measurement = error_time/CALIBRATION_SLOPE;
          Serial.print(averageTime);
          Serial.print(' ');
          Serial.println(measurement);
          lcd.clear();
          lcd.setCursor(0, 0);
          lcd.print(averageTime);
          lcd.print(' ');
          lcd.print((char)0);
          lcd.print(error_time);
          lcd.print(' ');
          lcd.print(char(B11100100));
          lcd.print("s");
          lcd.setCursor(0, 1);
          lcd.print(measurement);
          lcd.print(' ');
          lcd.print((char)0);
          lcd.print(error_measurement);
          lcd.print(" cm");
          averageTime = 0;
          averageSquaredTime = 0;
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
