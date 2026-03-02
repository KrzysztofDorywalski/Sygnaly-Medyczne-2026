import nidaqmx
from nidaqmx.constants import AcquisitionType
import keyboard  # Zainstaluj przez: pip install keyboard
import time

def acquire_signal(sample_rate=1000):
    """
    Akwizycja sygnału z kanału AI0 za pomocą NI USB-6000.
    
    :param sample_rate: Częstotliwość próbkowania (w Hz).
    """
    with nidaqmx.Task() as task:
        # Tworzenie kanału analogowego wejścia
        task.ai_channels.add_ai_voltage_chan("Dev1/ai0", min_val=-10.0, max_val=10.0)

        # Konfiguracja próbkowania w trybie ciągłym
        task.timing.cfg_samp_clk_timing(
            rate=sample_rate,
            sample_mode=AcquisitionType.CONTINUOUS
        )

        print("Rozpoczęcie akwizycji... (naciśnij 'q' aby zakończyć)")

        while True:
            try:
                # Odczyt jednego pomiaru
                voltage = task.read()
                print(f"Napięcie: {voltage:.5f} V")

                # Sprawdzenie, czy naciśnięto 'q' do zakończenia
                if keyboard.is_pressed('q'):
                    print("Zakończono akwizycję.")
                    break

                time.sleep(1 / sample_rate)

            except Exception as e:
                print(f"Wystąpił błąd: {e}")
                break

if __name__ == "__main__":
    acquire_signal()
