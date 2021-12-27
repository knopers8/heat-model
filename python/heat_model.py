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

# heat model modules
import hm_db
import hm_model

def computeError(reference, results):
  return sum(pow(reference - results, 2))

def getModelOptimizationFunction(config, t_begin, t_end):
  
  ub = hm_db.retrieveExternalConditions(config['influx-db-config'], t_begin, t_end)
  x12 = hm_db.retrieveKnownStates(config['influx-db-config'], t_begin, t_end)
  
  # TODO support any step
  t_begin = t_begin - (t_begin % 60)
  t_end = t_end - (t_end % 60)
  t_space = np.arange(t_begin, t_end, 60) # TODO parametrize step
  dt_space = pd.DatetimeIndex([ datetime.fromtimestamp(t, tz=pytz.UTC) for t in t_space ], freq='60S')
  
  def modelOptimizationFunction(params):
    print('params: ' + str(params))
    alfa, kappa, lambd, m, c = hm_model.matricesFromParameters(params[0:31])
    x_0 = params[31:]
    x_00 = x_0.T # [0]
    print('x_00 ' + str(x_00))
    A, K, L = hm_model.parametersToStateMatrices(alfa, kappa, lambd, m, c)
    
    ode_model = hm_model.make_ode_model(A, K, L, ub)
    num_sol = solve_ivp(ode_model, [t_begin, t_end], x_00, method='Radau', t_eval=t_space)
    X_num_sol = num_sol.y
    x1_num_sol = pd.Series(X_num_sol[0].T, index=dt_space)
    x2_num_sol = pd.Series(X_num_sol[1].T, index=dt_space)
       
    error = computeError(x12['x1'], x1_num_sol) + computeError(x12['x2'], x2_num_sol)
    print('error: ' + str(error))
    return error
    
  return modelOptimizationFunction

def runModel(config, t_begin, t_end):
  alfa, kappa, lambd, m, c = hm_model.matricesFromParameters(hm_model.defaultParameters())
  x_0 = hm_model.defaultInitialConditions()
  ub = hm_db.retrieveExternalConditions(config['influx-db-config'], t_begin, t_end)
  x12 = hm_db.retrieveKnownStates(config['influx-db-config'], t_begin, t_end)
  
  A, K, L = hm_model.parametersToStateMatrices(alfa, kappa, lambd, m, c)
  ode_model = hm_model.make_ode_model(A, K, L, ub)
  
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
  params_0 = hm_model.defaultParameters()
  params_0 = np.append(params_0, hm_model.defaultInitialConditions())
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