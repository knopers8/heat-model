
from influxdb import InfluxDBClient

from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import pytz
import sys
import json

def defaultParameters():
  ### all input parameters

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

  return alfa, kappa, lambd, m, c

def defaultInitialConditions():
  x_0 = np.array([
    [20],
    [18],
    [19],
    [18],
    [10],
    [8]
    ])
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
    
  print(A)
  print(K)
  print(L)
  return A, K, L


def make_ode_model(A, K, L, u, b):
  def model(t, x):
    dt = pytz.utc.localize(datetime.fromtimestamp(t)).isoformat()
    current_u = np.array([ [u[0].asof(dt)], [u[1].asof(dt)], [u[2].asof(dt)], [u[3].asof(dt)]])
    current_b = np.array([ [b[0].asof(dt)], [b[1].asof(dt)], [b[2].asof(dt)], [b[3].asof(dt)]])
    # print('current_u')
    # print(current_u)
    # print('current_b')
    # print(current_b)
    res = np.dot(A, x.T) + np.dot(K, current_u).T[0] + np.dot(L, current_b).T[0]
    # print(res)
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


def retrieveExternalConditions(db_config, t_start, t_end):
  u1 = retrieveSeriesInfluxDB(db_config, 'onewire', 'temperature', t_start, t_end, '')
  u2 = retrieveSeriesInfluxDB(db_config, 'bbmeteo', 'temperature', t_start, t_end, 'd8439cc8c1cd')
  u3 = retrieveSeriesInfluxDB(db_config, 'bbmeteo', 'temperature', t_start, t_end, 'f62ca793005e')
  u4 = retrieveSeriesInfluxDB(db_config, 'power_consumption', 'power', t_start, t_end, '')
  
  b1 = retrieveSeriesInfluxDB(db_config, 'bbmeteo', 'brightness', t_start, t_end, 'cea3118ce7ab').map(defaultUncoveredSensorLuxCalibration())
  b2 = retrieveSeriesInfluxDB(db_config, 'bbmeteo', 'brightness', t_start, t_end, 'f261555d69d9').map(defaultUncoveredSensorLuxCalibration())
  b3 = retrieveSeriesInfluxDB(db_config, 'bbmeteo', 'brightness', t_start, t_end, 'd8439cc8c1cd').map(defaultCoveredSensorLuxCalibration())
  b4 = retrieveSeriesInfluxDB(db_config, 'bbmeteo', 'brightness', t_start, t_end, 'f62ca793005e').map(defaultUncoveredSensorLuxCalibration())
  
  # i am sure it can be done smarter
  # (i don't know yet what to do about different sampling rates and missing points. just resample to one time domain?)
  u = np.array([ u1, u2, u3, u4 ], dtype=object)
  b = np.array([ b1, b2, b3, b4 ], dtype=object)
  return u, b


def retrieveKnownStates(db_config, t_start, t_end):
  x1 = retrieveSeriesInfluxDB(db_config, 'bbmeteo', 'temperature', t_start, t_end, 'cea3118ce7ab')
  x2 = retrieveSeriesInfluxDB(db_config, 'bbmeteo', 'temperature', t_start, t_end, 'f261555d69d9')
  return x1, x2


def storeInfluxDB():
  # todo: general method to store in influxdb
  print("todo")

def storeModelRun():
  #todo: store a model run
  print("todo")

def computeAvgDist(reference, results):
  # todo: compute some coeff measuring distance
  print("todo")

def runModel(config, t_begin, t_end, t_nsamples):
  alfa, kappa, lambd, m, c = defaultParameters()
  x_0 = defaultInitialConditions()  
  u, b = retrieveExternalConditions(config['influx-db-config'], t_begin, t_end)
  
  A, K, L = parametersToStateMatrices(alfa, kappa, lambd, m, c)
  ode_model = make_ode_model(A, K, L, u, b)
  
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



def main():
  #todo: run default stuff
  config_path = sys.argv[1]
  with open(config_path, "r") as config_json:
    config = json.load(config_json)
  
  runModel(config, 1639349078 - 2 * 24 * 60 * 60, 1639349078, 10000)

if __name__ == "__main__":
  exit(main())