# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 13:19:01 2023

@author: krzysztof
"""

import numpy as np
import math
from scipy import signal
import matplotlib.pyplot as plt

t = np.arange(0,2,0.001)
omega = 2*np.pi
A = 1
y = 0.5*(signal.square(omega*t)+1)  #przebieg prostokątny


N=100 #liczba harmonicznych
x=0.5
for k in range(1,N,2):
   x = x + 2*A/(k*np.pi)*np.sin(k*omega*t)

plt.plot(t,x,'--',t,y,'-') 
plt.title('rozkład przebiegu prostokątnego w szereg Fouriera') 
plt.grid 
#plt.axis([0 2 -0.1 1.1]);

k = np.arange(1,N,2)
Ak = np.absolute(2/(np.pi*k)*np.sin(0.5*np.pi*k))

plt.figure()
plt.stem(k,Ak);
plt.title('Charakterystyka amplitudowa');
