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
    5000    # m6
  ])
  
  params = np.array([1.65099043e-01, 1.02774422e+03, 1.09841448e+03, 3.01458070e+02,
    2.22826937e+02, 6.72509425e+02, 1.77124062e+03, 1.67233701e+02,
    7.78841039e+00, 5.46383483e+00, 7.57372958e+00, 2.05129289e+02,
    1.27446180e-02, 1.27860157e-02, 1.74204717e+01, 1.77821111e-02,
    4.97882611e+02, 1.38456100e+02, 1.70887374e+02, 1.60466920e-01,
    1.94468681e-01, 1.57122665e-01, 6.82519347e-01, 4.63661418e-02,
    8.81426749e-02, 1.35836775e+02, 2.26374016e+01, 5.61996328e+03,
    8.23528772e+04, 6.99492202e+04, 6.80298435e+04])
    
  params = np.array([2.01598404e-01, 1.34493388e+03, 1.97251579e+03, 3.98614790e+02,
 1.73951339e+02, 4.57706608e+02, 7.57193966e+01, 1.99140639e+02,
 5.33172015e+00, 7.50944177e+00, 8.54318818e+00, 3.27665011e+02,
 1.23844369e-02, 9.07104477e-03, 9.64776808e+00, 2.35990899e-02,
 2.49505961e+02, 1.03111176e+02, 4.02518900e+01, 1.30535166e-01,
 1.82427144e-01, 1.27492841e-01, 6.21972416e-01, 6.38328402e-02,
 2.75493898e-02, 1.43187395e+02, 2.54246117e+01, 4.68094399e+03,
 8.08070753e+04, 1.03388156e+05, 1.20973275e+05])
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
    (-10, 30)    # x6
    ]
  return bounds

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

  alfa = np.array([
    [0     , alfa12, alfa13, alfa14, alfa15,  alfa16],
    [alfa21,      0, alfa23, alfa24,      0,  alfa26],
    [alfa31, alfa32,      0, alfa34,      0,       0],
    [alfa14, alfa42, alfa43,      0, alfa45,  alfa46],
    [alfa15,      0,      0, alfa54,      0,       0],
    [alfa16, alfa62,      0, alfa64,      0,       0]
    ])

  kappa = np.array([
    [kappa11, kappa12, kappa13,    0],
    [kappa21,       0, kappa23,    0],
    [      0,       0,       0,    1],
    [kappa41,       0,       0,    0],
    [      0, kappa52,       0,    0],
    [      0,       0, kappa63,    0]
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

  return alfa, kappa, lambd, m, c

def defaultInitialConditions():
  x_0 = np.array([
    [20.3],
    [19.3],
    [19],
    [19],
    [15],
    [13]
    ])
  
  # x_0 = np.array([[24.44165186], [12.59187175], [16.73906938], [22.85770545], [15.060221467], [13.44287631]])
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
  def __init__(self, A, K, L):
    self.A = A
    self.K = K
    self.L = L
  
  def fromOptParameters(p):
    alfa, kappa, lambd, m, c = matricesFromParameters(p)
    A, K, L = parametersToStateMatrices(alfa, kappa, lambd, m, c)
    return Model(A, K, L)
  
  def makeCallback(self, ub):
    last_dt = ub.index[-1]
    def model(t, x):
      dt = datetime.fromtimestamp(t, tz=pytz.UTC).replace(second=0, microsecond=0)
      # print(dt)
      if dt > last_dt:
        dt = last_dt
      current_ub = ub.loc[dt]
      current_u = np.array([ current_ub[0:4] ]).T
      current_b = np.array([ current_ub[4:8] ]).T
      # import code
      # code.interact(local=locals())
      res = np.dot(self.A, x.T) + np.dot(self.K, current_u).T[0] + np.dot(self.L, current_b).T[0]
      return res

    return model
  
  def run(self, t_space, x_0, ub):
    x_00 = x_0.T # [0]
    # Radau shows less fluctuations when system is stabilized
    num_sol = solve_ivp(self.makeCallback(ub), [t_space[0], t_space[-1]], x_00, method='Radau', t_eval=t_space)
    
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
  x1_num_sol = pd.Series(X_num_sol[0].T, index=dt_space)
  x2_num_sol = pd.Series(X_num_sol[1].T, index=dt_space)
  x3_num_sol = pd.Series(X_num_sol[2].T, index=dt_space)
  x4_num_sol = pd.Series(X_num_sol[3].T, index=dt_space)
  x5_num_sol = pd.Series(X_num_sol[4].T, index=dt_space)
  x6_num_sol = pd.Series(X_num_sol[5].T, index=dt_space)

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