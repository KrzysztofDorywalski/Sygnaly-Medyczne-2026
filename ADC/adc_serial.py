import serial  # Import biblioteki do komunikacji szeregowej
import time

# Ustawienia portu (zmień 'COM3' na właściwy port dla twojego Arduino)
PORT = 'COM10'  # Windows: np. COM3, COM4 | Linux/macOS: np. /dev/ttyUSB0, /dev/ttyACM0
BAUD_RATE = 9600  # Taka sama prędkość jak w Arduino

try:
    # Inicjalizacja połączenia z Arduino
    ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Poczekaj na nawiązanie połączenia
    print("✅ Połączono z Arduino!")

    while True:
        try:
            data = ser.readline().decode('utf-8').strip()  # Odczytaj linię z portu
            if data:  # Jeśli dane nie są puste
                voltage = float(data)  # Konwersja na liczbę zmiennoprzecinkową
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
