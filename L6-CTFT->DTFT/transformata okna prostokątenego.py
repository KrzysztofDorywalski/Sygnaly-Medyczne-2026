# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 09:14:46 2024

@author: KD

Transformata okna prostokątego: X(w) = 2A/w * sin(w*T/2) = AT*sinc(wT/2)
"""
import numpy as np
import matplotlib.pyplot as plt

A = 1
T = 1

t = np.arange(-2,2,0.01)
x = np.zeros(len(t))

for i in range(len(t)):
    if t[i] >= -T/2 and t[i] <= T/2:
        x[i] = A

plt.subplot(211)
plt.plot(t,x)   #impuls prostokątny
plt.title('Impuls prostokątny')
plt.xlabel('t / s')
plt.ylabel('x(t)')

#Transforamta impulsu prostokątnego
w = np.arange(-10,10,0.05)
X = A*T*np.sinc(w*T/2)
plt.subplot(212)
plt.plot(w,X)
plt.title('Transformata impulsu prostokątnego')
plt.xlabel('$\omega$ / rad')
plt.ylabel('X($\omega$)')
plt.subplots_adjust(hspace=0.8)

#widmo amplitudowe i fazowe
ampl = np.abs(X)
arg = np.degrees(np.angle(X))
plt.figure()
plt.subplot(211)
plt.plot(w, ampl)
plt.title('widmo amplitudowe')
plt.ylabel('|X($\omega$|')
plt.xlabel('X($\omega$)')
plt.subplot(212)
plt.plot(w, arg)
plt.title('widmo fazowe')
plt.ylabel('$\phi$ / $\degree$ ')
plt.xlabel('X($\omega$)')
plt.subplots_adjust(hspace=0.8)