# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 14:59:13 2023

@author: krzysztof
"""
from numpy import *
from matplotlib.pyplot import *

#sygnał dyskretny
n = arange(0,8,1)
xn = [0, -1, -1, 0, 1, 1, 0, 0]
stem(n, xn)

#transformata Fouriera
omega = arange(-6,6,0.01)
Xw = -2*1j*exp(-1j*3*omega)*(sin(omega)+sin(2*omega))

#widmo amplitudowe
figure()
plot(omega, abs(Xw));
title('widmo amplitudowe');

#widmo fazowe
figure()
plot(omega, ((angle(Xw))*180)/pi);
title('widmo fazowe');
