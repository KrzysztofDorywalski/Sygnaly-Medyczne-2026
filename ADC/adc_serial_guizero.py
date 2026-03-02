import serial
import time
import matplotlib.pyplot as plt
import csv
from guizero import App, PushButton, Text

# --- Ustawienia portu ---
PORT = 'COM10'  # Windows: np. 'COM3', Linux/macOS: '/dev/ttyUSB0'
BAUD_RATE = 9600

# --- Inicjalizacja list ---
# Listy przechowujące CAŁĄ historię do zapisu w CSV
all_timestamps = []
all_voltages = []

# Listy ograniczane do 100 próbek (tylko na potrzeby wykresu)
plot_timestamps = []
plot_voltages = []

# Zmienne globalne stanu
running = False
start_time = 0

# --- Inicjalizacja wykresu ---
plt.ion()  # Tryb interaktywny
fig, ax = plt.subplots()
ax.set_xlabel("Czas (s)")
ax.set_ylabel("Napięcie (V)")
ax.set_title("Pomiar napięcia w czasie rzeczywistym")

# --- Funkcja zapisująca dane do pliku CSV ---
def save_to_csv():
    # Sprawdzenie, czy są jakiekolwiek dane do zapisu
    if not all_timestamps:
        print("Brak danych do zapisu.")
        return
        
    with open('dane_pomiarowe.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Czas (s)', 'Napięcie (V)'])
        for t, v in zip(all_timestamps, all_voltages):
            writer.writerow([t, v])
    print("✅ Dane zapisane do pliku dane_pomiarowe.csv")

# --- Funkcja odczytująca dane (wywoływana cyklicznie przez GUI) ---
def read_serial_data():
    if not running:
        return
        
    # Sprawdzamy czy w buforze portu szeregowego czekają jakieś dane
    if ser.in_waiting > 0:
        try:
            data = ser.readline().decode('utf-8').strip()
            if data:
                voltage = float(data)
                current_time = time.time() - start_time
                
                # 1. Zapis całościowy (do pliku)
                all_timestamps.append(current_time)
                all_voltages.append(voltage)

                # 2. Zapis bieżący (na wykres)
                plot_timestamps.append(current_time)
                plot_voltages.append(voltage)

                if len(plot_timestamps) > 100:
                    plot_timestamps.pop(0)
                    plot_voltages.pop(0)

                # 3. Aktualizacja GUI i konsoli
                result_text.value = f"Napięcie: {voltage:.2f} V"
                print(f"📟 Odczytane napięcie: {voltage:.2f} V")

                # 4. Bezpieczna aktualizacja wykresu (bez plt.pause!)
                ax.clear()
                ax.plot(plot_timestamps, plot_voltages, color="red", label="Napięcie (V)")
                ax.set_xlabel("Czas (s)")
                ax.set_ylabel("Napięcie (V)")
                ax.set_title("Pomiar napięcia w czasie rzeczywistym")
                ax.legend(loc="upper left")
                
                # Wymuszenie odświeżenia płótna wykresu bez przerywania pętli
                fig.canvas.draw()
                fig.canvas.flush_events()

        except ValueError:
            print("⚠️ Błąd konwersji danych - pominięto niepoprawny odczyt.")

# --- Funkcja zatrzymująca pomiar ---
def stop_measurement():
    global running
    running = False
    app.cancel(read_serial_data)  # Anulowanie cyklicznego odpytywania
    save_to_csv()
    status_text.value = "Pomiar zakończony. Dane zapisane."
    print("🛑 Zatrzymano pomiar i zapisano do CSV.")

# --- Funkcja rozpoczynająca pomiar ---
def start_measurement():
    global running, start_time
    if not running:  # Zabezpieczenie przed wielokrotnym kliknięciem
        running = True
        start_time = time.time()
        status_text.value = "Pomiar w trakcie..."
        
        # Zamiast pętli while, zlecamy aplikacji cykliczne wykonywanie funkcji
        # Tutaj: wywołuj read_serial_data co 50 milisekund
        app.repeat(50, read_serial_data)

# --- Inicjalizacja GUI ---
app = App("Pomiar Napięcia", width=400, height=300)

status_text = Text(app, text="Kliknij Start, aby rozpocząć pomiar.", size=12, color="blue", height=2)
result_text = Text(app, text="Napięcie: 0.00 V", size=14, color="red")

start_button = PushButton(app, command=start_measurement, text="Start", width=10, height=2)
stop_button = PushButton(app, command=stop_measurement, text="Stop", width=10, height=2)

# --- Uruchomienie połączenia i programu ---
try:
    ser = serial.Serial(PORT, BAUD_RATE, timeout=0.1) # timeout zmieniony na mniejszy dla płynności
    time.sleep(2)
    print("✅ Połączono z Arduino!")
    
    # Główna pętla aplikacji
    app.display()

except serial.SerialException:
    print("❌ Błąd: Nie można otworzyć portu szeregowego. Sprawdź nazwę PORTU.")
    status_text.value = "Błąd połączenia z urządzeniem."
    app.display() # Wyświetlamy GUI i tak, żeby użytkownik zobaczył błąd
except KeyboardInterrupt:
    print("\n🛑 Zakończono program z klawiatury.")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("🔒 Port szeregowy został poprawnie zamknięty.")