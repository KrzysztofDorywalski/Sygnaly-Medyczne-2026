const int analogPin = A0;

volatile bool sampleFlag = false;

void setup() {
  Serial.begin(115200);

  // konfiguracja Timer1
  cli(); // wyłącz przerwania

  TCCR1A = 0;
  TCCR1B = 0;

  TCNT1 = 0;

  // wartość porównania
  // 16 MHz / 8 prescaler = 2 MHz
  // 2 MHz * 0.0005 s = 1000
  OCR1A = 999;

  TCCR1B |= (1 << WGM12); // tryb CTC
  TCCR1B |= (1 << CS11);  // prescaler 8

  TIMSK1 |= (1 << OCIE1A); // włącz przerwanie

  sei(); // włącz przerwania
}

ISR(TIMER1_COMPA_vect) {
  sampleFlag = true;
}

void loop() {

  if (sampleFlag) {

    sampleFlag = false;

    int adcValue = analogRead(analogPin);

    Serial.write(0xAA);
    Serial.write(lowByte(adcValue));
    Serial.write(highByte(adcValue));
  }
}
