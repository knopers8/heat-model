
from influxdb import InfluxDBClient

from scipy.integrate import solve_ivp
from scipy.optimize import minimize
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import pytz
import sys
import json
import cProfile

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
  
  # params = np.array([2.42812581e-01,  9.84127387e+03,  5.89097487e+03,  1.52346061e+02,
  # 1.94061987e+02,  2.68282253e+02,  2.25041825e+02,  5.14563941e+02,
  # 3.94310265e+00,  4.10445269e+00,  1.14545698e+01,  1.74527036e+02,
  # 1.88303822e-02,  1.22621778e-02,  3.77766050e+01,  1.20549133e-02,
  # 5.97424661e+02, -3.74242412e+01,  7.55038580e+01,  4.10639069e-01,
  # 1.49637582e-01,  1.97919206e-01,  9.85689071e-01,  3.07577251e-02,
  # 3.76970877e-02,  9.19450196e+01,  3.16828111e+01,  3.99528762e+03,
  # 5.25225791e+04,  5.00342766e+03,  5.17384576e+03])
  return params

def validateParameters(params):

  # all parameters should be not less than 0
  if (any(p < 0 for p in params)):
    return False
  
  # todo: more will follow

  return True

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
    [19.5],
    [18],
    [18],
    [18],
    [10],
    [8]
    ])
  
  # x_0 = np.array([[18.44693111], [17.63445569], [18.27838006], [18.23274769], [6.88350227], [6.54061254]])
  return x_0

def defaultCoveredSensorLuxCalibration():
  return lambda m : 15000000.0 / ( 2550000.0 / m - 10000)
  
def defaultUncoveredSensorLuxCalibration():
  return lambda m : 5000000.0 / ( 2550000.0 / m - 10000)

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


def make_ode_model(A, K, L, ub):
  last_dt = ub.index[-1]
  def model(t, x):
    dt = datetime.fromtimestamp(t, tz=pytz.UTC).replace(second=0, microsecond=0)
    # print(dt)
    if dt > last_dt:
      dt = last_dt
    current_ub = ub.loc[dt]
    current_u = np.array([ current_ub[0:4] ]).T
    current_b = np.array([ current_ub[4:8] ]).T
    res = np.dot(A, x.T) + np.dot(K, current_u).T[0] + np.dot(L, current_b).T[0]
    return res

  return model

def retrieveSeriesInfluxDB(db_config, table, field, t_begin_s, t_end_s, address):
  ### establish a connection to the database
  client = InfluxDBClient(db_config['host'], db_config['port'], db_config['user'], db_config['password'], db_config['dbname'])
  client.ping()
  
  if len(field) == 0:
    field = "*"
  
  # hello injections!
  query = 'SELECT \"' + field + '\" '
  query += 'FROM \"' + table + '\" '
  query += 'WHERE time >= ' + str(t_begin_s) + 's AND time <= ' + str(t_end_s) + 's '
  if len(address):
    query += 'AND (\"address\" =~ /^' + address + '$/) '
  query += 'GROUP BY * ORDER BY ASC'
  print(query)

  result = client.query(query)
  
  # that is probably a very inefficient to transform the result to pandas series
  indices = []
  values = []
  for r in result: # that is just a wrapper with one element 'r'
    for entry in r:
      indices.append(pd.Timestamp(entry['time']))
      values.append(entry[field])
  
  print('Retrieved field ' + field + ' from table ' + table + ', got ' + str(len(values)) + ' entries')
  return pd.Series(values, index=indices)

def aggregateSeries(*series, freq):
  # i don't know why, but I have to use mean() before padding any values fwd and bckwd.
  df = pd.concat(series, axis=1).resample(freq, kind='timestamp').mean().fillna(method='ffill').fillna(method='bfill')
  return df

def retrieveExternalConditions(db_config, t_start, t_end):
  u1 = retrieveSeriesInfluxDB(db_config, 'onewire', 'temperature', t_start, t_end, '')
  u2 = retrieveSeriesInfluxDB(db_config, 'bbmeteo', 'temperature', t_start, t_end, 'd8439cc8c1cd')
  u3 = retrieveSeriesInfluxDB(db_config, 'bbmeteo', 'temperature', t_start, t_end, 'f62ca793005e')
  u4 = retrieveSeriesInfluxDB(db_config, 'power_consumption', 'power', t_start, t_end, '')
  u1.name = 'u1'
  u2.name = 'u2'
  u3.name = 'u3'
  u4.name = 'u4'
  
  b1 = retrieveSeriesInfluxDB(db_config, 'bbmeteo', 'brightness', t_start, t_end, 'cea3118ce7ab').map(defaultUncoveredSensorLuxCalibration())
  b2 = retrieveSeriesInfluxDB(db_config, 'bbmeteo', 'brightness', t_start, t_end, 'f261555d69d9').map(defaultUncoveredSensorLuxCalibration())
  b3 = retrieveSeriesInfluxDB(db_config, 'bbmeteo', 'brightness', t_start, t_end, 'd8439cc8c1cd').map(defaultCoveredSensorLuxCalibration())
  b4 = retrieveSeriesInfluxDB(db_config, 'bbmeteo', 'brightness', t_start, t_end, 'f62ca793005e').map(defaultUncoveredSensorLuxCalibration())
  b1.name = 'b1'
  b2.name = 'b2'
  b3.name = 'b3'
  b4.name = 'b4'
  
  df = aggregateSeries(u1, u2, u3, u4, b1, b2, b3, b4, freq='60S')

  return df


def retrieveKnownStates(db_config, t_start, t_end):
  x1 = retrieveSeriesInfluxDB(db_config, 'bbmeteo', 'temperature', t_start, t_end, 'cea3118ce7ab')
  x2 = retrieveSeriesInfluxDB(db_config, 'bbmeteo', 'temperature', t_start, t_end, 'f261555d69d9')
  
  x1.name = 'x1'
  x2.name = 'x2'
  return aggregateSeries(x1, x2, freq='60S')

def storeInfluxDB():
  # todo: general method to store in influxdb
  print("todo")

def storeModelRun():
  #todo: store a model run
  print("todo")

def computeError(reference, results):
  return sum(pow(reference - results, 2))

def getModelOptimizationFunction(config, t_begin, t_end):
  
  ub = retrieveExternalConditions(config['influx-db-config'], t_begin, t_end)
  x12 = retrieveKnownStates(config['influx-db-config'], t_begin, t_end)
  
  # TODO support any step
  t_begin = t_begin - (t_begin % 60)
  t_end = t_end - (t_end % 60)
  t_space = np.arange(t_begin, t_end, 60) # TODO parametrize step
  dt_space = pd.DatetimeIndex([ datetime.fromtimestamp(t, tz=pytz.UTC) for t in t_space ], freq='60S')
  
  def modelOptimizationFunction(params):
    print('params: ' + str(params))
    alfa, kappa, lambd, m, c = matricesFromParameters(params[0:31])
    x_0 = params[31:]
    x_00 = x_0.T # [0]
    print('x_00 ' + str(x_00))
    A, K, L = parametersToStateMatrices(alfa, kappa, lambd, m, c)
    
    ode_model = make_ode_model(A, K, L, ub)
    num_sol = solve_ivp(ode_model, [t_begin, t_end], x_00, method='Radau', t_eval=t_space)
    X_num_sol = num_sol.y
    x1_num_sol = pd.Series(X_num_sol[0].T, index=dt_space)
    x2_num_sol = pd.Series(X_num_sol[1].T, index=dt_space)
       
    error = computeError(x12['x1'], x1_num_sol) + computeError(x12['x2'], x2_num_sol)
    print('error: ' + str(error))
    return error
    
  return modelOptimizationFunction

def runModel(config, t_begin, t_end):
  alfa, kappa, lambd, m, c = matricesFromParameters(defaultParameters())
  x_0 = defaultInitialConditions()
  ub = retrieveExternalConditions(config['influx-db-config'], t_begin, t_end)
  x12 = retrieveKnownStates(config['influx-db-config'], t_begin, t_end)
  
  A, K, L = parametersToStateMatrices(alfa, kappa, lambd, m, c)
  ode_model = make_ode_model(A, K, L, ub)
  
  # TODO support any step
  t_begin = t_begin - (t_begin % 60)
  t_end = t_end - (t_end % 60)
  t_space = np.arange(t_begin, t_end, 60) # TODO parametrize step
  dt_space = pd.DatetimeIndex([ datetime.fromtimestamp(t, tz=pytz.UTC) for t in t_space ], freq='60S')
  x_00 = x_0.T[0]
  
  # Radau shows less fluctuations when system is stabilized
  print('simulation started')
  num_sol = solve_ivp(ode_model, [t_begin, t_end], x_00, method='Radau', t_eval=t_space)
  print('simulation finished')
  X_num_sol = num_sol.y
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
  plt.plot(x12['x1'], '-', linewidth=1, label='x1_real')
  plt.plot(x12['x2'], '-', linewidth=1, label='x2_real')

  plt.xlabel('t')
  plt.legend()
  
  print('x1 error: ' + str(computeError(x12['x1'], x1_num_sol)))
  print('x2 error: ' + str(computeError(x12['x2'], x2_num_sol)))
  plt.show()

def optimizeModel(config, t_begin, t_end):
  params_0 = defaultParameters()
  params_0 = np.append(params_0, defaultInitialConditions())
  modelOptFun = getModelOptimizationFunction(config, t_begin, t_end)
  res = minimize(modelOptFun, params_0, method='nelder-mead', options={'xatol': 1e-2, 'disp': True, 'maxiter' : 10000})
  print(res.x)
  

def main():
  config_path = sys.argv[1]
  with open(config_path, "r") as config_json:
    config = json.load(config_json)
  
  runModel(config, 1640341752 - 14 * 24 * 60 * 60, 1640341752)
  # optimizeModel(config, 1640341752 - 14 * 24 * 60 * 60, 1640341752)

if __name__ == "__main__":
  # res = cProfile.run('main()', sort='cumtime')
  res = main()
  exit(res)