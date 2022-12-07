import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

dT = 0.1
TotalTime = 10
Tin = np.linspace(0, TotalTime, round(TotalTime/dT) + 1)
m = 0.5
L = 0.45
g = 9.81
sys_tf = signal.TransferFunction([1], [m*L**2, 0, 2-m*g*L])
sys_tf = signal.tf2ss([1], [m*L**2, 0, 2-m*g*L])
print(sys_tf)

zero_input = np.zeros(Tin.shape) 
start_pos = 15 / 180.0 * np.pi 
Tout,yout,xout = signal.lsim(sys_tf, zero_input, Tin, X0=[0, start_pos/9.88]) 
plt.figure()
plt.plot(Tout, yout, 'b')
limit = 15 / 180.0 * np.pi
plt.plot([0, TotalTime], [limit, limit], 'r')
plt.plot([0, TotalTime], [-limit, -limit], 'r')

P = 0.8
I = 0.2
D = 0.2
PID_num = [D, P, I]
PID_den = [1, 0]
interm_num = np.convolve([1], PID_num)
interm_den = np.convolve([m*L**2, 0, 2-m*g*L], PID_den)
total_sys = signal.tf2ss(interm_den, np.polyadd(interm_den, interm_num))
print(total_sys)

# моделирование маятника с регулятором
Tout,yout,xout = signal.lsim(total_sys, zero_input, Tin, X0=[0, start_pos/9.88, 0])

plt.figure()
plt.plot(Tout, yout, 'b')
plt.plot([0, TotalTime], [limit, limit], 'r')
plt.plot([0, TotalTime], [-limit, -limit], 'r')

plt.show()