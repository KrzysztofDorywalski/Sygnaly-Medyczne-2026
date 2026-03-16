const int analogPin = A0;

const unsigned long intervalUs = 500; 
unsigned long previousMicros = 0;

void setup() {
  Serial.begin(115200);
}

void loop() {
  unsigned long currentMicros = micros();

  if (currentMicros - previousMicros >= intervalUs) {
    previousMicros += intervalUs; 

    int adcValue = analogRead(analogPin);

    Serial.write(0xAA);                 // marker startu ramki
    Serial.write(lowByte(adcValue));    // bajt młodszy
    Serial.write(highByte(adcValue));   // bajt starszy
  }
}
