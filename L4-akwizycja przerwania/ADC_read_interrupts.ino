const int analogPin = A0;

// Ustawienie częstotliwości (np. 500 Hz = 2000 mikrosekund)
const unsigned long intervalUs = 2000; 
unsigned long previousMicros = 0;

void setup() {
  Serial.begin(115200);
}

void loop() {
  unsigned long currentMicros = micros();

  // Sprawdzamy, czy upłynął już żądany czas
  if (currentMicros - previousMicros >= intervalUs) {
    // Ważne: dodajemy interwał do poprzedniej wartości, aby uniknąć błędów
    // kumulacji czasu (tzw. drift)
    previousMicros += intervalUs; 

    // Odczyt i wysyłka
    int adcValue = analogRead(analogPin);
    Serial.println(adcValue);
  }
}
