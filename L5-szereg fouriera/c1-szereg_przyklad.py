# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 09:38:54 2023

@author: krzysztof
"""

#Liczba harmonicznych w odtworzeniu sygnału prostokątnego, unipolarnego
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

#unipolarna fala prostokątna
t = np.arange(0, 2, 0.001)
A = 1
omega = 2*np.pi
y = 0.5*(signal.square(omega*t)+1)

#5 harmonicznych
x = 0.5 + 2*A/np.pi*np.sin(omega*t) + 2*A/(3*np.pi)*np.sin(3*omega*t) + 2*A/(5*np.pi)*np.sin(5*omega*t)
plt.subplot(211)
plt.plot(t,x,'--',t,y,'-')
plt.grid()
plt.ylabel('x(t)')
plt.title('4 harmoniczne')

#11 harmonicznych
x = x + 2*A/(7*np.pi)*np.sin(7*omega*t) + 2*A/(9*np.pi)*np.sin(9*omega*t) + 2*A/(11*np.pi)*np.sin(11*omega*t)
+2*A/(13*np.pi)*np.sin(13*omega*t)+2*A/(15*np.pi)*np.sin(15*omega*t)+2*A/(17*np.pi)*np.sin(17*omega*t)
+2*A/(19*np.pi)*np.sin(19*omega*t)
plt.subplot(212)
plt.plot(t,x,'--',t,y,'-')
plt.grid()
plt.ylabel('x(t)')
plt.title('11 harmonicznych')


