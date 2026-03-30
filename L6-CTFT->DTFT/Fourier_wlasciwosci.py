# -*- coding: utf-8 -*-
"""
Created on Mon May 12 13:34:27 2025

Właciwoci transformaty Fouriera
"""

import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft, fftfreq, fftshift

# Parametry sygnału
N = 1024
T = 1.0 / 1000
t = np.linspace(-0.5, 0.5, N, endpoint=False)
f = fftshift(fftfreq(N, d=T))

# Funkcja bazowa: sygnał gaussowski
def signal(t):
    return np.exp(-100 * t**2)

# Transformaty
def fourier_transform(x):
    X = fft(x)
    X = fftshift(X)
    X_mag = np.abs(X)
    X_mag /= np.max(X_mag)
    return X_mag

# 1. Skalowanie czasu: x(at) → (1/|a|) X(f/a)
x1 = signal(t)
x1_slow = signal(0.5 * t)     # rozciągnięty czas
x1_fast = signal(2 * t)       # ściśnięty czas

# 2. Przesunięcie w czasie: x(t - t0) → X(f) * e^{-j2πft0}
t_shift = 0.1
x2 = signal(t)
x2_shifted = signal(t - t_shift)

# 3. Przesunięcie w częstotliwości: x(t) * e^{j2πf0t} → X(f - f0)
f0 = 100
x3 = signal(t)
x3_modulated = x3 * np.exp(1j * 2 * np.pi * f0 * t)

# FFT
X1 = fourier_transform(x1)
X1_slow = fourier_transform(x1_slow)
X1_fast = fourier_transform(x1_fast)

X2 = fourier_transform(x2)
X2_shifted = fourier_transform(x2_shifted)

X3 = fourier_transform(x3)
X3_modulated = fourier_transform(x3_modulated)

# Rysowanie
fig, axs = plt.subplots(3, 2, figsize=(12, 10))

# 1. Skalowanie czasu
axs[0, 0].plot(t, x1, label='Oryginalny')
axs[0, 0].plot(t, x1_slow, label='Rozciągnięty (a=0.5)', linestyle='--')
axs[0, 0].plot(t, x1_fast, label='Ściśnięty (a=2)', linestyle=':')
axs[0, 0].set_title("Skalowanie czasu – dziedzina czasu")
axs[0, 0].legend()
axs[0, 0].grid()

axs[0, 1].plot(f, X1, label='Oryginalny')
axs[0, 1].plot(f, X1_slow, label='Rozciągnięty (a=0.5)', linestyle='--')
axs[0, 1].plot(f, X1_fast, label='Ściśnięty (a=2)', linestyle=':')
axs[0, 1].set_title("Skalowanie czasu – widmo")
axs[0, 1].legend()
axs[0, 1].grid()

# 2. Przesunięcie w czasie
axs[1, 0].plot(t, x2, label='Oryginalny')
axs[1, 0].plot(t, x2_shifted, label=f'Przesunięcie o {t_shift}s', linestyle='--')
axs[1, 0].set_title("Przesunięcie w czasie – dziedzina czasu")
axs[1, 0].legend()
axs[1, 0].grid()

axs[1, 1].plot(f, X2, label='Oryginalny')
axs[1, 1].plot(f, X2_shifted, label='Przesunięty', linestyle='--')
axs[1, 1].set_title("Przesunięcie w czasie – widmo (moduł)")
axs[1, 1].legend()
axs[1, 1].grid()

# 3. Przesunięcie w częstotliwości
axs[2, 0].plot(t, np.real(x3), label='Oryginalny')
axs[2, 0].plot(t, np.real(x3_modulated), label=f'Modulacja {f0}Hz', linestyle='--')
axs[2, 0].set_title("Przesunięcie w częstotliwości – dziedzina czasu")
axs[2, 0].legend()
axs[2, 0].grid()

axs[2, 1].plot(f, X3, label='Oryginalny')
axs[2, 1].plot(f, X3_modulated, label=f'Modulowany {f0}Hz', linestyle='--')
axs[2, 1].set_title("Przesunięcie w częstotliwości – widmo")
axs[2, 1].legend()
axs[2, 1].grid()

plt.tight_layout()
plt.show()
