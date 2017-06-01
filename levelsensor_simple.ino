int pulsePin = 3;
int capPin = 4;

float pulseTime;
bool pulseIsHigh = false;
bool capIsHigh = false;
const int N_SAMPLES = 100;
int currentSample = 0;
float averageTime = 0;

void setup() {
  Serial.begin(9600);
  pinMode(pulsePin, INPUT);
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
