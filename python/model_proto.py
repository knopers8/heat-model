
import numpy as np
import matplotlib.pyplot as plt

from scipy.integrate import solve_ivp

### all input parameters

# alfa [ W / K ]
alfa = np.array([
  [0   , 0.15, 6250, 8325, 525,  262],
  [0.15,    0, 1250, 2000,   0,  188],
  [6250, 1250,    0,    4,   0,    0],
  [8325, 2000,    4,    0, 6.7, 7.95],
  [525 ,    0,    0,  6.7,   0,    0],
  [262 ,  188,    0, 7.95,   0,    0]
  ])

kappa = np.array([
  [102.5, 0.025, 0.0125,    0],
  [24.34,     0, 0.0125,    0],
  [    0,     0,      0,    1],
  [  272,     0,      0,    0],
  [    0,   525,      0,    0],
  [    0,     0,    525,    0]
  ])

lambd = np.array([
  [     0,     0,     0,     0],
  [     0,     0,     0,     0],
  [ 0.208, 0.208,     0,     0],
  [ 0.708, 0.696,     0,     0],
  [     0,     0, 0.041,     0],
  [     0,     0,     0, 0.041]
  ])

# masses [kg]
m = np.array([133.23, 26.22, 3000, 37000, 5000, 5000])
# heat capacity [ J / (kg K) ]
c = np.array([1000, 1000, 1500, 880, 880, 880])

x_0 = np.array([
  [20],
  [22],
  [19],
  [18],
  [15],
  [10]
  ])


### compute differential equation matrices

# all elements but diagonals just get alfa, then we divide all rows by (m_i * c_i)
A = alfa
for i in range(len(alfa)):
  A[i,i] = - sum(alfa[i]) - sum(kappa[i]) - sum(lambd[i])

for i in range(len(alfa)):
  A[i] = A[i] / m[i] / c[i]

K = kappa
L = lambd

for i in range(len(alfa)):
  K[i] = K[i] / m[i] / c[i]
  L[i] = L[i] / m[i] / c[i]

# dump input data
u = np.array([
  [30],
  [15],
  [10],
  [100]
  ])

b = np.array([
  [100],
  [100],
  [10000],
  [5000]
  ])

def ode_model(t, x):
  return np.dot(A, x.T) + np.dot(K, u).T[0] + np.dot(L, b).T[0]

t_begin=50.
t_end=500.
t_nsamples=1000
t_space = np.linspace(t_begin, t_end, t_nsamples)
x_00 = x_0.T[0]

# Radau shows less fluctuation when system is stabilized
num_sol = solve_ivp(ode_model, [t_begin, t_end], x_00, method='Radau', dense_output=True)

X_num_sol = num_sol.sol(t_space)
x1_num_sol = X_num_sol[0].T
x2_num_sol = X_num_sol[1].T
x3_num_sol = X_num_sol[2].T
x4_num_sol = X_num_sol[3].T
x5_num_sol = X_num_sol[4].T
x6_num_sol = X_num_sol[5].T

plt.figure()
plt.plot(t_space, x1_num_sol, '-', linewidth=1, label='x1')
plt.plot(t_space, x2_num_sol, '-', linewidth=1, label='x2')
plt.plot(t_space, x3_num_sol, '-', linewidth=1, label='x3')
plt.plot(t_space, x4_num_sol, '-', linewidth=1, label='x4')
plt.plot(t_space, x5_num_sol, '-', linewidth=1, label='x5')
plt.plot(t_space, x6_num_sol, '-', linewidth=1, label='x6')


plt.xlabel('t')
plt.legend()
plt.show()