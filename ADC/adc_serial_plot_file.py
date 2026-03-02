import serial
import time
import matplotlib.pyplot as plt
import csv
from datetime import datetime

# 🔹 Ustawienia portu (dostosuj do swojego systemu)
PORT = 'COM6'  # Windows: np. 'COM3', Linux/macOS: '/dev/ttyUSB0'
BAUD_RATE = 9600  # Musi być taki sam jak w Arduino

# 🔹 Inicjalizacja list do przechowywania danych
timestamps = []
voltages = []

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

# 🔹 Inicjalizacja wykresu
plt.ion()  # Tryb interaktywny
fig, ax = plt.subplots()
ax.set_xlabel("Czas (s)")
ax.set_ylabel("Napięcie (V)")
ax.set_title("Pomiar napięcia w czasie rzeczywistym")
line, = ax.plot([], [], color="red", label="Napięcie (V)")
ax.legend()

try:
    # 🔹 Utworzenie pliku CSV
    create_csv(file_name)

    # 🔹 Połączenie z Arduino
    ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Poczekaj na stabilizację połączenia
    print("✅ Połączono z Arduino!")

    start_time = time.time()

    while True:
        try:
            # 🔹 Odczyt linii z portu szeregowego
            data = ser.readline().decode('utf-8').strip()
            if data:
                voltage = float(data)  # Konwersja na liczbę
                current_time = time.time() - start_time  # Czas od startu

                # 🔹 Dodanie danych do listy
                timestamps.append(current_time)
                voltages.append(voltage)

                # 🔹 Zapis danych do pliku na bieżąco
                save_to_csv(file_name, f"{current_time:.3f}", f"{voltage:.5f}")

                # 🔹 Ograniczenie liczby próbek na wykresie (dla wydajności)
                if len(timestamps) > 100:
                    timestamps.pop(0)
                    voltages.pop(0)

                # 🔹 Aktualizacja wykresu
                line.set_xdata(timestamps)
                line.set_ydata(voltages)
                ax.relim()
                ax.autoscale_view()
                plt.pause(0.01)

                # 🔹 Wydruk wyniku na konsoli
                print(f"📟 Odczytane napięcie: {voltage:.2f} V")

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
