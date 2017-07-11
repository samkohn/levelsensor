#include <LiquidCrystal.h>

const int pulsePin = 2;
const int capPin = 3;

bool pulseIsHigh = true;
bool capIsHigh = true;

const int N_SAMPLES = 500;
const bool EXT_REF = false;
const unsigned int INT_REF_FREQ = 140; // Hz
const float CALIBRATION_SLOPE = 2.5; // us/cm
const float CALIBRATION_INTERCEPT = 321; // us

int currentSample = 0;
unsigned int pulseTime = 0;
float averageTime = 0;
float averageSquaredTime = 0;

LiquidCrystal lcd(7, 8, 9, 10, 11, 12);
const byte plusMinus[8] = {
  0b00100,
  0b00100,
  0b11111,
  0b00100,
  0b00100,
  0b00000,
  0b11111,
  0b00000
};

void reset_all_pins() {
  // Sets all pins to a known state
  for ( int pin = 0; pin < 20; pin++ ) {
    pinMode(pin, INPUT_PULLUP);
  }
}

void print_to_lcd(float timeAverage, float timeError, float measurement, float measurementError) {
  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print(timeAverage);
  lcd.print(' ');
  lcd.write(byte(0));
  lcd.print(timeError);
  lcd.print(' ');
  lcd.print(char(B11100100));
  lcd.print("s");

  lcd.setCursor(0, 1);
  lcd.print(measurement);
  lcd.print(' ');
  lcd.write(byte(0));
  lcd.print(measurementError);
  lcd.print(" cm");
}

void setup() {
  reset_all_pins();

  Serial.begin(9600);

  lcd.begin(16, 2);
  lcd.createChar(0, plusMinus);
  lcd.print("Starting up...");

  // Set up input/output pins
  if ( !EXT_REF ) {
    pinMode(pulsePin, OUTPUT);
    tone(pulsePin, INT_REF_FREQ);
  } else {
    pinMode(pulsePin, INPUT);
  }
  pinMode(capPin, INPUT);
}

void read_level_once() {
  while (true) {
    if (!pulseIsHigh && !capIsHigh) {
      // Wait for pulse to go high
      int pulseVal = digitalRead(pulsePin);
      if (pulseVal == HIGH) {
        pulseTime = micros();
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
          unsigned int currentTime = micros() - pulseTime;
          averageTime = averageTime + (float)(currentTime) / N_SAMPLES;
          averageSquaredTime = averageSquaredTime + (float)(currentTime) * (float)(currentTime) / N_SAMPLES;
          currentSample++;
        }
        if (currentSample == N_SAMPLES) {
          // Reset
          currentSample = 0;
          float measurement = (averageTime - CALIBRATION_INTERCEPT) / CALIBRATION_SLOPE;
          float error_time = sqrt(averageSquaredTime - averageTime * averageTime);
          float error_measurement = error_time / CALIBRATION_SLOPE;
          Serial.print(averageTime);
          Serial.print(' ');
          Serial.println(measurement);
          print_to_lcd(averageTime, error_time, measurement, error_measurement);
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


