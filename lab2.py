import numpy as np
import math
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

p_num = 101
b_pos = np.logspace(-7, 7, p_num)
b_neg = -np.logspace(-7, 7, p_num)
a = 5

# Система на границе устойчивости (колебательная)
Ps_pos = [[0, 0] for i in range(p_num)]
for i in range(p_num):
    z, p, k = signal.tf2zpk([a, 1], [b_pos[i], 0, 1])
    Ps_pos[i][0] = p[0]
    Ps_pos[i][1] = p[1]
fg, ax = plt.subplots()
ax.plot(np.real(Ps_pos), np.imag(Ps_pos), '.')
plt.title('Полюса системы на границе устойчивости')

# Система не устойчива
Ps_neg = [[0, 0] for i in range(p_num)]
for i in range(p_num):
    z, p, k = signal.tf2zpk([a, 1], [b_neg[i], 0, 1])
    Ps_neg[i][0] = p[0]
    Ps_neg[i][1] = p[1]
fg, ax = plt.subplots()
ax.plot(np.real(Ps_neg), np.imag(Ps_neg), '.')
plt.title('Полюса неустойчивой системы')

# Подадим на вход незамкнутой колебательной системы ступеньку. a = 5, b_1 = 3
freq = 15.6
b_1 = 3
test_RC_o_1 = signal.lti([a, 1], [b_1, 0, 1])
T = np.linspace(0, 400.0/freq, 2001)
S_Hev = [1 for t in T]
# Конечная по времени ступенька
#S_Hev_1 = [int(t < len(T) // 2) for t in range(len(T))]
Tout_o, yout_o, xout_o = signal.lsim(test_RC_o_1, S_Hev, T)
plt.figure()
plt.plot(Tout_o, yout_o)
plt.title('Реакция колебательной системы на ступеньку')

# Подадим на вход незамкнутой неустойчивой системы ступеньку. a = 5, b = -3
b_2 = -1
test_RC_o_2 = signal.lti([a, 1], [b_2, 0, 1])
Tout_o, yout_o, xout_o = signal.lsim(test_RC_o_2, S_Hev, T)
plt.figure()
plt.plot(Tout_o, yout_o)
plt.title('Реакция неустойчивой системы на ступеньку')

# Подадим на вход замкнутой изначально колебательной системы ступеньку. a = 5, b = 3
test_RC_c_1 = signal.lti([a, 1], [b_1, a, 2])
Tout_c, yout_c, xout_c = signal.lsim(test_RC_c_1, S_Hev, T)
plt.figure()
plt.plot(Tout_c, yout_c)
plt.title('Реакция изн. колеб. системы с отрицательно обратной связью')

# Подадим на вход замкнутой изначально неустойчивой системы ступеньку. a = 5, b = -3
test_RC_c_2 = signal.lti([a, 1], [b_2, a, 2])
Tout_c, yout_c, xout_c = signal.lsim(test_RC_c_2, S_Hev, T)
plt.figure()
plt.plot(Tout_c, yout_c)
plt.title('Реакция изн. неуст. системы с отрицательно обратной связью')

#Построим графики АЧХ, ФЧХ для незамкнутой колебательной системы
W, mag, phase = signal.bode(test_RC_o_1)
fs = [0.5*w/math.pi for w in W]
plt.figure()
plt.semilogx(fs, mag)
plt.title('АЧХ незамкн. колеб. системы')

plt.figure()
plt.semilogx(fs, phase)
plt.title('ФЧХ незамкн. колеб. системы')

#Построим графики АЧХ, ФЧХ для незамкнутой неустойчивой системы
W, mag, phase = signal.bode(test_RC_o_2)
fs = [0.5*w/math.pi for w in W]
plt.figure()
plt.semilogx(fs, mag)
plt.title('АЧХ незамк. неуст. системы')

plt.figure()
plt.semilogx(fs, phase)
plt.title('ФЧХ незамкн. неуст. системы')

#Построим графики АЧХ, ФЧХ для замкнутой изначально колебательной системы
W, mag, phase = signal.bode(test_RC_c_1)
fs = [0.5*w/math.pi for w in W]
plt.figure()
plt.semilogx(fs, mag)
plt.title('АЧХ замкн. изначально колеб. системы')

plt.figure()
plt.semilogx(fs, phase)
plt.title('ФЧХ замкн. изначально колеб. системы')

#Построим графики АЧХ, ФЧХ для замкнутой изначально неустойчивой системы
W, mag, phase = signal.bode(test_RC_c_2)
fs = [0.5*w/math.pi for w in W]
plt.figure()
plt.semilogx(fs, mag)
plt.title('АЧХ замк. изначально неуст. системы')

plt.figure()
plt.semilogx(fs, phase)
plt.title('ФЧХ замкн. изначально неуст. системы')

plt.show()