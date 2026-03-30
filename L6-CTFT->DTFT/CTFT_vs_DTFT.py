# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 12:27:49 2023

@author: krzysztof
""" 
from numpy import *
from matplotlib.pyplot import *

subplots_adjust(hspace=1.2)

#sygnał ciągły - analiza czasowa
alfa = 0.8
t = linspace(0,10*alfa,10000)
sig = exp(-alfa*t)
subplot(321), plot(t, sig, 'r--')
axis([0, 10*alfa, 0, 1.1])
title('Sygnał ciągły'), xlabel('t [s]')
grid

#Sygnał ciągły - analiza częstotliwościowa
f_c = linspace(-10*2*pi, 10*2*pi, 10000)
w = 2*pi*f_c
widmo_c = 1./(alfa+1j*f_c)
modul_c = abs(widmo_c)
subplot(322), plot(f_c/(2*pi), modul_c/max(modul_c),'r-')
title('Widmo ampl. sygnału ciągłego'), xlabel('f [Hz]')
grid
axis([-10, 10, 0, 1.1])

#sygnał dyskretny fp=16 - analiza czasowa
fs = 16
N=100
Ts=1/fs
n=arange(0,N)
#n=(0:N-1)
sig=exp(-alfa*Ts*n)
subplot(323), stem(n*Ts,sig,'b.')
title('Sygnał dyskretny, f_s=16Hz'), xlabel('t [s]'), grid
axis([0, 10*alfa, 0, 1.1])

#sygnał dyskretny fp=16 - analiza częstotliwościowa
Tsc=Ts;
Nc=1000;
a=exp(-alfa*Tsc);
f=linspace(-10,10,Nc);
widmo_d = 1./(1-a*exp(-1j*(2*pi*f*Tsc)));
widmo_d=abs(widmo_d);
subplot(324),plot(f,widmo_d/max(widmo_d))
title('Widmo ampl. sygnału dyskretnego'), xlabel('f [Hz]')
grid
axis([-10, 10, 0, 1.1])

#sygnał dyskretny fp=5 - analiza czasowa
fs = 5
Ts=1/fs
n=arange(0,N)
sig=exp(-alfa*Ts*n)
subplot(325), stem(n*Ts,sig,'b.')
title('Sygnał dyskretny, f_s=5Hz'), xlabel('t [s]'), grid
axis([0, 10*alfa, 0, 1.1])

#sygnał dyskretny fp=5 - analiza częstotliwościowa
Tsc=Ts;
a=exp(-alfa*Tsc);
f=linspace(-10,10,Nc);
widmo_d = 1./(1-a*exp(-1j*(2*pi*f*Tsc)));
widmo_d=abs(widmo_d);
subplot(326),plot(f,widmo_d/max(widmo_d))
title('Widmo ampl. sygnału dyskretnego'), xlabel('f [Hz]')
grid
axis([-10, 10, 0, 1.1])
