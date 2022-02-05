import numpy as np
import pandas as pd
from datetime import datetime
import pytz
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

import hm_db

def defaultParameters():
  params = np.array([
    0.15,   # alfa12, alfa21
    6250,   # alfa13, alfa31
    8325,   # alfa14, alfa41
    525,    # alfa15, alfa51
    262,    # alfa16, alfa61
    1250,   # alfa23, alfa32
    2000,   # alfa24, alfa42
    188,    # alfa26, alfa62
    4,      # alfa34, alfa43
    6.7,    # alfa45, alfa54
    7.95,   # alfa46, alfa64
    102.5,  # kappa11
    0.025,  # kappa12
    0.0125, # kappa13
    24.34,  # kappa21
    0.0125, # kappa23
    272,    # kappa41
    525,    # kappa52
    525,    # kappa63
    0.208,  # lambd31
    0.208,  # lambd32
    0.708,  # lambd41
    0.696,  # lambd42
    0.041,  # lambd53
    0.041,  # lambd64
    133.23, # m1
    26.22,  # m2
    3000,   # m3
    37000,  # m4
    5000,   # m5
    5000,   # m6
    7740,   # kappa45
    19      # u5
  ])
  
  params = np.array([1.33758942e-01, 6.30322266e+03, 1.81029269e+04, 5.07136835e+02,
       1.31151021e+02, 5.99866959e+02, 8.75570457e+02, 2.81840221e+02,
       4.88317737e+00, 9.24198862e+00, 1.30290635e+01, 5.41873097e+02,
       3.03546410e-02, 1.98936687e-02, 6.02826058e+01, 1.41978776e-02,
       5.72704642e+02, 3.17590268e+02, 5.30050155e+02, 8.26040957e-01,
       6.60308750e-01, 1.03864460e+00, 6.98628044e-01, 3.02197692e-02,
       3.32126315e-02, 1.60802667e+02, 2.45195741e+01, 1.34717976e+04,
       2.47330026e+05, 1.29893382e+04, 5.88553559e+03, 8.64079175e+02,
       1.98642488e+01])
     
   
  # params = np.array([1.53090562e-01, 5.14782533e+03, 8.09896167e+03, 5.25000000e+02,
       # 2.62000000e+02, 1.05006921e+03, 1.64801224e+03, 8.74731401e+02,
       # 4.23826429e+00, 6.67436088e+00, 9.86492470e+00, 5.26253647e+02,
       # 2.55225853e-02, 1.20014759e-02, 1.15730447e+02, 1.16948014e-02,
       # 2.72000000e+02, 5.25000000e+02, 5.25000000e+02, 2.08000000e-01,
       # 2.08000000e-01, 7.08000000e-01, 6.96000000e-01, 4.10000000e-02,
       # 4.10000000e-02, 1.29899132e+02, 2.29396675e+01, 6.24865589e+03,
       # 3.70000000e+04, 5.00000000e+03, 5.00000000e+03, 2.00000000e+03,
       # 1.90000000e+01])
  return params

def saveParameters(filepath, params):
  np.save(filepath, params)

def readParameters(filepath):
  return np.load(filepath)

def bounds():
  bounds = [
    (0.0001, 100),   # alfa12, alfa21
    (0.0001, 100000),   # alfa13, alfa31
    (0.0001, 100000),   # alfa14, alfa41
    (0.0001, 10000),    # alfa15, alfa51
    (0.0001, 10000),    # alfa16, alfa61
    (0.0001, 100000),   # alfa23, alfa32
    (0.0001, 100000),   # alfa24, alfa42
    (0.0001, 10000),    # alfa26, alfa62
    (0.0001, 1000),      # alfa34, alfa43
    (0.0001, 1000),    # alfa45, alfa54
    (0.0001, 1000),   # alfa46, alfa64
    (0.0001, 10000),  # kappa11
    (0.0001, 10),  # kappa12
    (0.0001, 10), # kappa13
    (0.0001, 1000),  # kappa21
    (0.0001, 10), # kappa23
    (0.0001, 10000),    # kappa41
    (0.0001, 10000),    # kappa52
    (0.0001, 10000),    # kappa63
    (0.0001, 10),  # lambd31
    (0.0001, 10),  # lambd32
    (0.0001, 10),  # lambd41
    (0.0001, 10),  # lambd42
    (0.0001, 10),  # lambd53
    (0.0001, 10),  # lambd64
    (1, 1000), # m1
    (1, 200),  # m2
    (100, 30000),   # m3
    (1000, 1000000),  # m4
    (100, 100000),   # m5
    (100, 100000),    # m6
    (10, 25),    # x1
    (10, 25),    # x2
    (0, 30),    # x3
    (0, 30),    # x4
    (-10, 30),    # x5
    (-10, 30),    # x6
    (0.0001, 50000),# kappa45
    (10, 25)      # u5
    ]
  return bounds

def boundsMinMax():
  min = []
  max = []
  for b in bounds():
    min.append(b[0])
    max.append(b[1])
  return (min, max)

def matricesFromParameters(params):
  alfa12 = alfa21 = params[0]
  alfa13 = alfa31 = params[1]
  alfa14 = alfa41 = params[2]
  alfa15 = alfa51 = params[3]
  alfa16 = alfa61 = params[4]
  alfa23 = alfa32 = params[5]
  alfa24 = alfa42 = params[6]
  alfa26 = alfa62 = params[7]
  alfa34 = alfa43 = params[8]
  alfa45 = alfa54 = params[9]
  alfa46 = alfa64 = params[10]
  kappa11 = params[11]
  kappa12 = params[12]
  kappa13 = params[13]
  kappa21 = params[14]
  kappa23 = params[15]
  kappa41 = params[16]
  kappa52 = params[17]
  kappa63 = params[18]
  lambd31 = params[19]
  lambd32 = params[20]
  lambd41 = params[21]
  lambd42 = params[22]
  lambd53 = params[23]
  lambd64 = params[24]
  m1 = params[25]
  m2 = params[26]
  m3 = params[27]
  m4 = params[28]
  m5 = params[29]
  m6 = params[30]
  kappa45 = params[31]
  u5 = params[32]

  alfa = np.array([
    [0     , alfa12, alfa13, alfa14, alfa15,  alfa16],
    [alfa21,      0, alfa23, alfa24,      0,  alfa26],
    [alfa31, alfa32,      0, alfa34,      0,       0],
    [alfa14, alfa42, alfa43,      0, alfa45,  alfa46],
    [alfa15,      0,      0, alfa54,      0,       0],
    [alfa16, alfa62,      0, alfa64,      0,       0]
    ])

  kappa = np.array([
    [kappa11, kappa12, kappa13,    0,       0],
    [kappa21,       0, kappa23,    0,       0],
    [      0,       0,       0,    1,       0],
    [kappa41,       0,       0,    0, kappa45],
    [      0, kappa52,       0,    0,       0],
    [      0,       0, kappa63,    0,       0]
    ])

  lambd = np.array([
    [       0,       0,       0,       0],
    [       0,       0,       0,       0],
    [ lambd31, lambd32,       0,       0],
    [ lambd41, lambd42,       0,       0],
    [       0,       0, lambd53,       0],
    [       0,       0,       0, lambd64]
    ])

  # masses [kg]
  m = np.array([m1, m2, m3, m4, m5, m6])
  # heat capacity [ J / (kg K) ]
  # we do not parametrize those, because they have exactly the same influence on A, K, L as m
  # so we avoid increasing degrees of freedom
  c = np.array([1000, 1000, 1500, 880, 880, 880])

  return alfa, kappa, lambd, m, c, u5

def defaultInitialConditions():
  x_0 = np.array([
    [20.3],
    [19.3],
    [19.6],
    [19.5],
    [15],
    [14.8]
    ])
    
  
  # x_0 = np.array([ 
    # [2.0570339e+01],
    # [1.90451733e+01],
    # [2.17531881e+01],
    # [2.18510327e+01],
    # [1.89070891e+01],
    # [1.75501882e+01]])
  return x_0

def parametersToStateMatrices(alfa, kappa, lambd, m, c):
  ### compute differential equation matrices

  # all elements but diagonals just get an alfa, then we divide all rows by (m_i * c_i)
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
  
  return A, K, L


class Model:
  def __init__(self, A, K, L, u5):
    self.A = A
    self.K = K
    self.L = L
    self.u5 = u5
  
  def fromOptParameters(p):
    alfa, kappa, lambd, m, c, u5 = matricesFromParameters(p)
    A, K, L = parametersToStateMatrices(alfa, kappa, lambd, m, c)
    return Model(A, K, L, u5)
  
  def makeCallback(self, ub):
    last_dt = ub.index[-1]
    def model(t, x):
      dt = datetime.fromtimestamp(t, tz=pytz.UTC).replace(second=0, microsecond=0)
      # print(dt)
      if dt > last_dt:
        dt = last_dt
      current_ub = ub.loc[dt]
      current_u = np.array([ current_ub[0:5] ]).T # we take one element more to make room for u5
      current_u[4] = self.u5 
      current_b = np.array([ current_ub[4:8] ]).T
      # import code
      # code.interact(local=locals())
      res = np.dot(self.A, x.T) + np.dot(self.K, current_u).T[0] + np.dot(self.L, current_b).T[0]
      return res

    return model
  
  def run(self, t_space, x_0, ub):
    # x_00 = x_0.T # [0]
    # Radau shows less fluctuations when system is stabilized
    num_sol = solve_ivp(self.makeCallback(ub), [t_space[0], t_space[-1]], x_0, method='Radau', t_eval=t_space)
    
    return num_sol

def prepareTime(t_begin, t_end):
  # TODO support any step
  t_begin = t_begin - (t_begin % 60)
  t_end = t_end - (t_end % 60)
  t_space = np.arange(t_begin, t_end, 60) # TODO parametrize step
  dt_space = pd.DatetimeIndex([ datetime.fromtimestamp(t, tz=pytz.UTC) for t in t_space ], freq='60S')
  return t_space, dt_space

def visualizeRun(solution, references):
  X_num_sol = solution.y
  dt_space = solution.dt_space
  x1_num_sol = pd.Series(X_num_sol[0].T, index=dt_space, name='x1')
  x2_num_sol = pd.Series(X_num_sol[1].T, index=dt_space, name='x2')
  x3_num_sol = pd.Series(X_num_sol[2].T, index=dt_space, name='x3')
  x4_num_sol = pd.Series(X_num_sol[3].T, index=dt_space, name='x4')
  x5_num_sol = pd.Series(X_num_sol[4].T, index=dt_space, name='x5')
  x6_num_sol = pd.Series(X_num_sol[5].T, index=dt_space, name='x6')

  plt.figure()
  plt.plot(x1_num_sol, '-', linewidth=1, label='x1')
  plt.plot(x2_num_sol, '-', linewidth=1, label='x2')
  plt.plot(x3_num_sol, '-', linewidth=1, label='x3')
  plt.plot(x4_num_sol, '-', linewidth=1, label='x4')
  plt.plot(x5_num_sol, '-', linewidth=1, label='x5')
  plt.plot(x6_num_sol, '-', linewidth=1, label='x6')
  for ref in references:
    plt.plot(ref, '-', linewidth=1, label=ref.name)

  plt.xlabel('t')
  plt.legend()
  
  plt.show()