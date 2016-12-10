int pulsePin = 3;
int capPin = 4;
const int PULSE_THRESHOLD = 190;
const int CAP_THRESHOLD = 580;
unsigned long pulseTime;
bool pulseIsHigh = false;
bool capIsHigh = false;
unsigned long delays[100];
const int DELAYS_TO_SAVE = 50;
unsigned int delays_index = 0;
int current_value = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(pulsePin, INPUT);
  pinMode(capPin, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(!pulseIsHigh && !capIsHigh) {
    // Wait for pulse to go high
    int pulseVal = digitalRead(pulsePin);
    if(pulseVal == HIGH) {
      pulseTime = micros();
      pulseIsHigh = true;
    }
  }
  if(pulseIsHigh && !capIsHigh) {
    // Wait for cap to go high
    int capVal = digitalRead(capPin);
    if(capVal == HIGH) {
      // Save the time delay
      unsigned long dt = micros() - pulseTime;
      capIsHigh = true;
      delays[delays_index] = dt;
      ++delays_index;
      if(delays_index >= DELAYS_TO_SAVE) {
        delays_index = 0;
        // calculate the total delay
        unsigned long sum = 0;
        for(unsigned int i = 0; i < DELAYS_TO_SAVE; ++i) {
          sum += delays[i];
        }
        int value = ((int)sum-8500)/550;
        if(value != current_value) {
          Serial.println(value);
          current_value = value;
        }
      }
    }
  }
  if(pulseIsHigh && capIsHigh) {
    // Wait for pulse to go low
    int pulseVal = digitalRead(pulsePin);
    if(pulseVal == LOW) {
      pulseIsHigh = false;
      capIsHigh = false;
    }
  }
}
