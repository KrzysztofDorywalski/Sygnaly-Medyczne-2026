import nidaqmx
from nidaqmx.constants import AcquisitionType
import time

def acquire_signal(sample_rate=1000, duration=5):
    """
    Akwizycja sygnału z kanału AI0 za pomocą NI USB-6000.
    
    :param sample_rate: Częstotliwość próbkowania (w Hz).
    :param duration: Czas trwania akwizycji (w sekundach).
    """
    with nidaqmx.Task() as task:
        # Tworzenie kanału analogowego wejścia
        task.ai_channels.add_ai_voltage_chan("Dev1/ai0", min_val=-10.0, max_val=10.0)

        # Konfiguracja próbkowania w trybie ciągłym
        task.timing.cfg_samp_clk_timing(
            rate=sample_rate,
            sample_mode=AcquisitionType.CONTINUOUS
        )

        print("Rozpoczęcie akwizycji...")

        start_time = time.time()
        while time.time() - start_time < duration:
            # Odczyt jednego pomiaru
            voltage = task.read()
            print(f"Napięcie: {voltage:.5f} V")
            time.sleep(1 / sample_rate)

        print("Akwizycja zakończona.")

if __name__ == "__main__":
    acquire_signal()
