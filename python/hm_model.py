import numpy as np
import pandas as pd
from datetime import datetime
import pytz
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import csv

import hm_db

def defaultParameters():

  params = {
    'alfa12' : 0.15,
    'alfa13' : 6250,
    'alfa14' : 8325,
    'alfa15' : 525,
    'alfa16' : 262,
    'alfa23' : 1250,
    'alfa24' : 2000,
    'alfa26' : 188,
    'alfa34' : 4,
    'alfa45' : 6.7,
    'alfa46' : 7.95,
    'kappa11' : 102.5,
    'kappa12' : 0.025,
    'kappa13' : 0.0125,
    'kappa21' : 24.34,
    'kappa23' : 0.0125,
    'kappa41' : 272,
    'kappa52' : 525,
    'kappa63' : 525,
    'lambd31' : 0.208,
    'lambd32' : 0.208,
    'lambd41' : 0.708,
    'lambd42' : 0.696,
    'lambd53' : 0.041,
    'lambd64' : 0.041,
    'm1' : 133.23,
    'm2' : 26.22,
    'm3' : 3000,
    'm4' : 37000,
    'm5' : 5000,
    'm6' : 5000,
    'kappa45' : 7740,
    'u5' : 19
  }
  
  params = {'alfa12': 0.133758942, 'alfa13': 6303.22266, 'alfa14': 18102.9269,
    'alfa15': 507.136835, 'alfa16': 131.151021, 'alfa23': 599.866959, 'alfa24': 875.570457,
    'alfa26': 281.840221, 'alfa34': 4.88317737, 'alfa45': 9.24198862, 'alfa46': 13.0290635,
    'kappa11': 541.873097, 'kappa12': 0.030354641, 'kappa13': 0.0198936687,
    'kappa21': 60.2826058, 'kappa23': 0.0141978776, 'kappa41': 572.704642,
    'kappa52': 317.590268, 'kappa63': 530.050155, 'lambd31': 0.826040957,
    'lambd32': 0.66030875, 'lambd41': 1.0386446, 'lambd42': 0.698628044,
    'lambd53': 0.0302197692, 'lambd64': 0.0332126315, 'm1': 160.802667,
    'm2': 24.5195741, 'm3': 13471.7976, 'm4': 247330.026, 'm5': 12989.3382,
    'm6': 5885.53559, 'kappa45': 864.079175, 'u5': 19.8642488
    }
   
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
  csvfile = open(filepath, 'w')
  writer = csv.DictWriter(csvfile, fieldnames = params.keys())
  writer.writeheader()
  writer.writerows([params])
  csvfile.close()

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
  alfa12 = alfa21 = params['alfa12']
  alfa13 = alfa31 = params['alfa13']
  alfa14 = alfa41 = params['alfa14']
  alfa15 = alfa51 = params['alfa15']
  alfa16 = alfa61 = params['alfa16']
  alfa23 = alfa32 = params['alfa23']
  alfa24 = alfa42 = params['alfa24']
  alfa26 = alfa62 = params['alfa26']
  alfa34 = alfa43 = params['alfa34']
  alfa45 = alfa54 = params['alfa45']
  alfa46 = alfa64 = params['alfa46']
  kappa11 = params['kappa11']
  kappa12 = params['kappa12']
  kappa13 = params['kappa13']
  kappa21 = params['kappa21']
  kappa23 = params['kappa23']
  kappa41 = params['kappa41']
  kappa52 = params['kappa52']
  kappa63 = params['kappa63']
  lambd31 = params['lambd31']
  lambd32 = params['lambd32']
  lambd41 = params['lambd41']
  lambd42 = params['lambd42']
  lambd53 = params['lambd53']
  lambd64 = params['lambd64']
  m1 = params['m1']
  m2 = params['m2']
  m3 = params['m3']
  m4 = params['m4']
  m5 = params['m5']
  m6 = params['m6']
  kappa45 = params['kappa45']
  u5 = params['u5']

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