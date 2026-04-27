# -*- coding: utf-8 -*-
"""
Created on Tue May  7 09:07:35 2024

@author: KD
"""

import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
import scipy.fftpack as fft


gitara = "Alesis-Fusion-Clean-Guitar-C3.wav"
audio = "MIN7TH.wav"
glos = "glos_Weronika.wav"

#otwarcie pliku audio
rate1, data1 = wavfile.read('Alesis-Fusion-Clean-Guitar-C3.wav')
mono_data1 = np.mean(data1, axis=1)
N1 = len(data1)

#obliczenie widma
widmo1 = np.fft.fft(mono_data1)
widmo1 = np.abs(widmo1)
fk1 = np.fft.fftfreq(N1, 1/rate1)

#wizualizacja
plt.plot(fk1[:N1//2], widmo1[:N1//2])
plt.title('fft z numpy')
plt.xlabel('f / Hz'); plt.ylabel('|H(w)|')

glos = "glos.wav"

#otwarcie pliku audio
rate1, data1 = wavfile.read(glos)
mono_data1 = np.mean(data1, axis=1)
N1 = len(data1)

#obliczenie widma
widmo1 = np.fft.fft(mono_data1)
widmo1 = np.abs(widmo1)
fk1 = np.fft.fftfreq(N1, 1/rate1)

#wizualizacja
plt.figure()
plt.plot(fk1[:N1//2], widmo1[:N1//2])
plt.title('fft z numpy')
plt.xlabel('f / Hz'); plt.ylabel('|H(w)|')


'''
#fft z scipy
F = fft.fft(mono_data)
freq = fft.fftfreq(N, 1/rate)
mask = np.where(freq>=0)
plt.figure()
plt.plot(freq[mask],np.abs(F[mask])/N); plt.title('fft z scipy')
plt.xlabel('f / Hz'); plt.ylabel('|H(w)|')
'''