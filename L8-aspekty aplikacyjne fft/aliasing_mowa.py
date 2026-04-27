import os
import numpy as np
from scipy.io import wavfile
from scipy.signal import decimate

def apply_aliasing_to_speech(input_file="mowa.wav"):
    # Sprawdzenie, czy plik istnieje
    if not os.path.exists(input_file):
        print(f"BŁĄD: Nie znaleziono pliku '{input_file}'!")
        print("Nagraj krótki plik ze swoim głosem i nazwij go 'mowa.wav'.")
        return

    # 1. Wczytanie oryginalnego pliku audio
    fs, data = wavfile.read(input_file)
    
    # Jeśli plik jest stereo (2 kanały), bierzemy tylko lewy kanał do testu (mono)
    if len(data.shape) > 1:
        data = data[:, 0]
        
    # 2. Parametry próbkowania
    # Zmniejszymy częstotliwość próbkowania 6-krotnie. 
    # Jeśli oryginalny plik ma 44100 Hz lub 48000 Hz, nowy będzie miał ok. 7350 Hz lub 8000 Hz.
    dowsnample_factor = 6 
    fs_new = fs // dowsnample_factor
    
    # 3. ZŁA METODA: Brutalne cięcie próbek (Wywołanie ALIASINGU)
    # Bierzemy co 6-tą próbkę. Wysokie częstotliwości z głosu (np. sybilanty "s", "sz") 
    # nie mają miejsca i "zawijają się" w dół pasma, tworząc metaliczny hałas.
    y_aliased = data[::dowsnample_factor]
    
    # 4. DOBRA METODA: Prawidłowa decymacja (Ochrona przed aliasingiem)
    # Funkcja decimate z biblioteki scipy najpierw aplikuje filtr anty-aliasingowy 
    # (usuwa zbyt wysokie częstotliwości), a dopiero potem odrzuca próbki.
    y_anti_aliased = decimate(data, dowsnample_factor, zero_phase=True)
    y_anti_aliased = np.int16(y_anti_aliased) # Konwersja na odpowiedni format audio
    
    # 5. Zapis wyników
    wavfile.write("01_mowa_oryginalna.wav", fs, data)
    wavfile.write("02_mowa_aliasing_METALICZNA.wav", fs_new, y_aliased)
    wavfile.write("03_mowa_poprawna_STTLUMIONA.wav", fs_new, y_anti_aliased)
    
    print("Zakończono sukcesem!\n")
    print(f"Oryginalna jakość: {fs} Hz")
    print(f"Zdegradowana jakość: {fs_new} Hz\n")
    print("Odsłuchaj pliki i porównaj:")
    print("- '02_mowa_aliasing_METALICZNA.wav' - usłyszysz cyfrowe, dzwoniące artefakty.")
    print("- '03_mowa_poprawna_STTLUMIONA.wav' - głos będzie brzmiał jak przez stary telefon stacjonarny (brak wysokich tonów), ale pozostanie czysty i zrozumiały.")

if __name__ == "__main__":
    apply_aliasing_to_speech("mowa.wav")