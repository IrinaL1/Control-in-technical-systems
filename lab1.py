import math
from tokenize import triple_quoted
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

freq_1 = 5.22
freq_2 = 15.6
test_RC = signal.lti([5, 1], [-3, 0, 1])

T_1 = np.linspace(0, 10.0/freq_1, 1001)
T_2 = np.linspace(0, 10.0/freq_2, 1001)
S_1 = [math.sin(t*2*math.pi*freq_1) for t in T_1] #freq_1, A = 1
Tout_1, yout_1, xout_1 = signal.lsim(test_RC, S_1, T_1)

S_2 = [10*math.sin(t*2*math.pi*freq_1) for t in T_1] #freq_1, A = 10
Tout_2, yout_2, xout_2 = signal.lsim(test_RC, S_2, T_1)

S_3 = [math.sin(t*2*math.pi*freq_2) for t in T_2] #freq_2, A = 1
Tout_3, yout_3, xout_3 = signal.lsim(test_RC, S_3, T_2)

#Посмотрим, как меняется выходной сигнал при изменении амплитуды входного сигнала

plt.figure() #график входного сигнала с амплитудой 1, частотой freq_1
plt.plot(T_1, S_1)
plt.figure() #график выходного сигнала
plt.plot(Tout_1, yout_1)

plt.figure() #график входного сигнала с амплитудой 10, частотой freq_1
plt.plot(T_1, S_2)
plt.figure() #график выходного сигнала
plt.plot(Tout_2, yout_2)

#Посмотрим, как меняется выходной сигнал при изменении частоты входного сигнала

plt.figure() #график входного сигнала с амплитудой 1, частотой freq_2
plt.plot(T_2, S_3)
plt.figure() #график выходного сигнала
plt.plot(Tout_3, yout_3)

W, mag, phase = signal.bode(test_RC)
fs = [0.5*w/math.pi for w in W]
a = 5
b = -3

#Функции A(w) и \Phi(w) теоретически посчитанные
A = [math.sqrt((a**2*w**2 + 1))/(1 - b*w**2) for w in W] 
lg_A = [20*math.log(i, 10) for i in A]
phi = [math.atan(a*w) for w in W]
phi_deg = [180*i/math.pi for i in phi]

#Сравниваем амплитуды 
plt.figure()
plt.semilogx(fs, mag)
plt.semilogx(fs, lg_A)

#Сравниваем фазы
plt.figure()
plt.semilogx(fs, phase)
plt.semilogx(fs, phi_deg)

#Подаем на вход ступеньку и сравниваем выход с графиком переходной функции
S_Hev = [1 for t in T_1] 
Tout_4, yout_4, xout_4 = signal.lsim(test_RC, S_Hev, T_1)
H = [1-(1 + a/math.sqrt(abs(b))) * math.exp(t/math.sqrt(abs(b))) / 2 - (1 - a/math.sqrt(abs(b))) * math.exp(-t/math.sqrt(abs(b))) / 2 for t in T_1]
plt.figure()
plt.plot(Tout_4, yout_4)
plt.plot(Tout_4, H)

plt.show()