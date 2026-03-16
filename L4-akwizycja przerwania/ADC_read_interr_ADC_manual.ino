const byte analogPin = 0;   // A0

volatile uint16_t adcValue;
volatile bool newSample = false;

void setup() {

  Serial.begin(115200);

  cli();  // wyłącz przerwania

  // ---------- ADC konfiguracja ----------

  ADMUX = 0;
  ADMUX |= (1 << REFS0);      // referencja AVcc
  ADMUX |= analogPin;         // kanał ADC0

  ADCSRA = 0;
  ADCSRA |= (1 << ADEN);      // włącz ADC
  ADCSRA |= (1 << ADIE);      // przerwanie ADC

  // prescaler 32 → ~38.5 kSPS
  ADCSRA |= (1 << ADPS2) | (1 << ADPS0);

  // Auto trigger
  ADCSRA |= (1 << ADATE);

  // Timer1 Compare Match B jako trigger
  ADCSRB = 0;
  ADCSRB |= (1 << ADTS2) | (1 << ADTS0);

  // ---------- Timer1 konfiguracja ----------

  TCCR1A = 0;
  TCCR1B = 0;

  // tryb CTC
  TCCR1B |= (1 << WGM12);

  // prescaler 8
  TCCR1B |= (1 << CS11);

  // 2000 Hz
  OCR1A = 999;
  OCR1B = 999;

  // start ADC
  ADCSRA |= (1 << ADSC);

  sei(); // włącz przerwania
}


ISR(ADC_vect) {

  adcValue = ADC;
  newSample = true;
}


void loop() {

  if (newSample) {

    newSample = false;

    Serial.write(0xAA);
    Serial.write(lowByte(adcValue));
    Serial.write(highByte(adcValue));
  }
}
