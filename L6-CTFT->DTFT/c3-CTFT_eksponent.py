# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 16:06:16 2023

@author: krzys
"""

#widmo amplitudowe i fazowe transformaty Fouriera sygnału wykładniczego
#x(t)=e^(-alfa*t);
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

A=10
alfa=2
t=np.linspace(0,10*alfa,10000);

#sygnał ciągły
s = A*np.exp(-alfa*t);
plt.subplot(311);
plt.plot(t,s,'r');
plt.xlim(0,10.1);
plt.title('Sygnał ciągły')
plt.xlabel('t / s');
plt.grid

#analiza częstotliwościowa
f=np.linspace(-10*2*np.pi,10*2*np.pi,10000)
w=2*np.pi*f
widmo = A/(alfa + 1j*f)
#widmo = A/(alfa+w)
modul = np.absolute(widmo);
faza= np.angle(widmo);
plt.subplot(312); plt.plot(f/(2*np.pi), modul/max(modul),'r-');
plt.title('Widmo amplitudowe'), plt.xlabel('f / Hz');
plt.grid
plt.subplot(313), plt.plot(f/(2*np.pi), faza/max(faza));
plt.title('Widmo fazowe'), plt.xlabel('f / Hz');
plt.grid
plt.subplots_adjust(hspace=0.8)

