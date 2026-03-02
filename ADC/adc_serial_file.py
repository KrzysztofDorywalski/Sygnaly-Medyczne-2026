import serial
import time
import csv
from datetime import datetime

# 🔹 Ustawienia portu (dostosuj do swojego systemu)
PORT = 'COM9'  # Windows: np. 'COM3', Linux/macOS: '/dev/ttyUSB0'
BAUD_RATE = 9600  # Musi być taki sam jak w Arduino

# 🔹 Generowanie unikalnej nazwy pliku z datą i godziną
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
file_name = f"dane_pomiarowe_{timestamp}.csv"

# 🔹 Funkcja tworząca plik CSV i zapisująca dane
def create_csv(file_name):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Czas (s)', 'Napięcie (V)'])
    print(f"✅ Plik CSV utworzony: {file_name}")

def save_to_csv(file_name, timestamp, voltage):
    with open(file_name, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, voltage])

try:
    # 🔹 Utworzenie pliku CSV
    create_csv(file_name)

    # 🔹 Połączenie z Arduino
    ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Poczekaj na stabilizację połączenia
    print("✅ Połączono z Arduino!")

    start_time = time.time()
    sample_count = 0  # Licznik próbek

    while True:
        try:
            # 🔹 Odczyt linii z portu szeregowego
            data = ser.readline().decode('utf-8').strip()
            if data:
                voltage = float(data)  # Konwersja na liczbę
                current_time = time.time() - start_time  # Czas od startu
                sample_count += 1  # Zwiększ licznik próbek

                # 🔹 Zapis danych do pliku na bieżąco
                save_to_csv(file_name, f"{current_time:.3f}", f"{voltage:.5f}")

                # 🔹 Obliczanie szybkości próbkowania
                sampling_rate = sample_count / current_time if current_time > 0 else 0

                # 🔹 Wydruk wyniku na konsoli
                print(f"📟 Czas: {current_time:.3f} s | Napięcie: {voltage:.5f} V | Szybkość próbkowania: {sampling_rate:.2f} Hz")

        except ValueError:
            print("⚠️ Błąd konwersji danych - pominięto niepoprawny odczyt.")
        except KeyboardInterrupt:
            print("\n🛑 Zakończono program.")
            break

except serial.SerialException:
    print("❌ Błąd: Nie można otworzyć portu szeregowego.")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
    print("🔒 Port szeregowy zamknięty.")
