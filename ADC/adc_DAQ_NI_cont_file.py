import nidaqmx
from nidaqmx.constants import AcquisitionType
import keyboard  # Zainstaluj przez: pip install keyboard
import time
import csv
from datetime import datetime

def acquire_signal(sample_rate=1000, file_name="pomiar.csv"):
    """
    Akwizycja sygnału z kanału AI0 za pomocą NI USB-6000 i zapis do pliku CSV.
    
    :param sample_rate: Częstotliwość próbkowania (w Hz).
    :param file_name: Nazwa pliku wynikowego.
    """
    # Tworzenie pliku CSV z nagłówkiem
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Czas", "Napięcie (V)"])  # Nagłówek

        with nidaqmx.Task() as task:
            # Tworzenie kanału analogowego wejścia
            task.ai_channels.add_ai_voltage_chan("Dev1/ai0", min_val=-10.0, max_val=10.0)

            # Konfiguracja próbkowania w trybie ciągłym
            task.timing.cfg_samp_clk_timing(
                rate=sample_rate,
                sample_mode=AcquisitionType.CONTINUOUS
            )

            print(f"Rozpoczęcie akwizycji... (naciśnij 'q' aby zakończyć)")
            start_time = time.time()

            while True:
                try:
                    # Odczyt jednego pomiaru
                    voltage = task.read()
                    current_time = time.time() - start_time
                    print(f"Czas: {current_time:.3f} s | Napięcie: {voltage:.5f} V")

                    # Zapis do pliku
                    writer.writerow([f"{current_time:.3f}", f"{voltage:.5f}"])

                    # Sprawdzenie, czy naciśnięto 'q' do zakończenia
                    if keyboard.is_pressed('q'):
                        print("Zakończono akwizycję.")
                        break

                    time.sleep(1 / sample_rate)

                except Exception as e:
                    print(f"Wystąpił błąd: {e}")
                    break

if __name__ == "__main__":
    # Generowanie unikalnej nazwy pliku z datą i godziną
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"pomiar_{timestamp}.csv"
    acquire_signal(file_name=file_name)
qq