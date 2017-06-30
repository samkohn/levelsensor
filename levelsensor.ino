/*
int pulsePin = 3;
int capPin = 4;
const int PULSE_THRESHOLD = 190;
const int CAP_THRESHOLD = 580;
// Edit the offset and us_per_cm to calibrate the conversion
// from microseconds to cm.
float offset = 0;
float us_per_cm = 1;

float pulseTime;
bool pulseIsHigh = false;
bool capIsHigh = false;
const int LEN_DELAYS = 100;
float delays[LEN_DELAYS];
const int DELAYS_TO_SAVE = 100;
unsigned int delays_index = 0;
int current_value = 0;
const int STILL_MEASURING = -31415;
const int NUM_TIMESTAMPS = 100;
unsigned long timestamps[NUM_TIMESTAMPS];
unsigned long timestamp_index = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(pulsePin, INPUT);
  pinMode(capPin, INPUT);
  Serial.setTimeout(10000);
  // Quick and dirty calibration
  
}
  
void erase_delays_array() {
  for(int i = 0; i < LEN_DELAYS; ++i) {
    delays[i] = 0;
  }
}

void print_delays_array(int n) {
  Serial.print("[ ");
  if(n > 0) {
    Serial.print(delays[0]);
  }
  for(int i = 1; i < n; ++i) {
    Serial.print(", ");
    Serial.print(delays[i]);
  }
  Serial.print(" ]");
}

void print_timestamps_array(int n) {
  Serial.print("[ ");
  if(n > 0) {
    Serial.print(timestamps[0]);
  }
  for(int i = 1; i < n; ++i) {
    Serial.print(", ");
    Serial.print(timestamps[i]);
  }
  Serial.print(" ]");
}

int read_level_once() {
  int value = STILL_MEASURING;
  while(value == STILL_MEASURING) {
    value = one_read_cycle(false);
  }
  return value;
}

void loop() {
  read_level_once();
  //print_delays_array(DELAYS_TO_SAVE);
  //Serial.println("");
  Serial.flush();
  //delay(500);
  //Serial.println(read_level_once());
}
int one_read_cycle(bool calibrate) {
  if (!pulseIsHigh && !capIsHigh) {
    // Wait for pulse to go high
    int pulseVal = digitalRead(pulsePin);
    if (pulseVal == HIGH) {
      pulseTime = float(micros());
      pulseIsHigh = true;
    }
    return STILL_MEASURING;
  }
  if (pulseIsHigh && !capIsHigh) {
    // Wait for cap to go high
    int capVal = digitalRead(capPin);
    if (capVal == HIGH) {
      // Save the time delay
      float dt = float(micros()) - pulseTime;
      capIsHigh = true;
      delays[delays_index] = dt;
      ++delays_index;
      if (delays_index >= DELAYS_TO_SAVE) {
        delays_index = 0;
        // calculate the total delay
        unsigned long sum = 0;
        for (unsigned int i = 0; i < DELAYS_TO_SAVE; ++i) {
          sum += delays[i];
        }
        // This is where the final value is computed
        float value = (sum/DELAYS_TO_SAVE - offset)/us_per_cm;
        // If you want more info printed to the screen, you can add that here
        Serial.print(millis());
        Serial.print(' ');
        Serial.println(value);

        // This code is still a work in progress and is not executed yet.
        if(calibrate) {
          Serial.println("------Calibration-------");
          Serial.print("Number of readouts:  ");
          Serial.println(DELAYS_TO_SAVE);
          Serial.print("Total time measured: ");
          Serial.println(sum);
          Serial.print("Time per readout:    ");
          Serial.println(sum/DELAYS_TO_SAVE);
          Serial.println("Measured value:      " + String(value) + " cm"); 
          Serial.print("Enter new offset per readout (currently is");
          Serial.print(offset);
          Serial.println(")");
          float new_offset = Serial.parseFloat();
          Serial.print("Enter new microseconds-per-cm conversion factor (currently is");
          Serial.print(us_per_cm);
          Serial.println(")");
          float new_us_per_cm = Serial.parseFloat();
          Serial.print("The new value is ");
          Serial.println( (sum/DELAYS_TO_SAVE - new_offset)/new_us_per_cm);
          Serial.println("Type 1 to accept the changes or 0 to revert");
          bool save = Serial.parseInt() == 1;
          if(save) {
            offset = new_offset;
            us_per_cm = new_us_per_cm;
          }
        }
        return value;
      }
    }
    return STILL_MEASURING;
  }
  if (pulseIsHigh && capIsHigh) {
    // Wait for pulse to go low
    int pulseVal = digitalRead(pulsePin);
    if (pulseVal == LOW) {
      pulseIsHigh = false;
      capIsHigh = false;
    }
    return STILL_MEASURING;
  }
}

void track_timestamps() {
  if(timestamp_index < NUM_TIMESTAMPS) {
    timestamps[timestamp_index] = micros();
    ++timestamp_index;
  }
  else {
    print_timestamps_array(NUM_TIMESTAMPS);
    Serial.println("");
    timestamp_index = 0;
  }
}

*/