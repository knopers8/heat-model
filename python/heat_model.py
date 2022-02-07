from scipy.optimize import minimize
from scipy import optimize
import numpy as np
from datetime import datetime
import pandas as pd
import pytz
import sys
import json
import cProfile

# heat model modules
import hm_db
import hm_model
import hm_opt

def runModel(config, t_begin, t_end):
  p = hm_model.defaultParameters()
  
  x_0 = hm_model.defaultInitialConditions().T[0]
  t_space, dt_space = hm_model.prepareTime(t_begin, t_end)
  ub = hm_db.retrieveExternalConditions(config['influx-db-config'], t_begin, t_end)
  x12 = hm_db.retrieveKnownStates(config['influx-db-config'], t_begin, t_end)

  cont = True
  while cont:
    model = hm_model.Model.fromOptParameters(p)
    solution = model.run(t_space, x_0, ub)
    solution.dt_space = dt_space
    
    X_num_sol = solution.y
    x1_num_sol = pd.Series(X_num_sol[0].T, index=dt_space)
    x2_num_sol = pd.Series(X_num_sol[1].T, index=dt_space)
    print('x1 error: ' + str(hm_opt.computeError(x12['x1'], x1_num_sol)))
    print('x2 error: ' + str(hm_opt.computeError(x12['x2'], x2_num_sol)))
    
    hm_model.visualizeRun(solution, [x12['x1'], x12['x2']])
    import code
    code.interact(local=locals())
  
  return solution

def optimizeModel(config, t_begin, t_end):
  params_0 = np.array([p for p in hm_model.defaultParameters().values()])
  params_0 = np.append(params_0, hm_model.defaultInitialConditions())
  modelOptFun = hm_opt.getModelOptimizationFunction(config, t_begin, t_end)
  res = minimize(modelOptFun, params_0, method='nelder-mead', options={'fatol': 1.0, 'disp': True, 'maxiter' : 1000})
  # res = minimize(modelOptFun, params_0, method='trust-constr', bounds=hm_model.bounds())
  # res = optimize.shgo(modelOptFun, hm_model.bounds())
  print(res)
  print(dict(zip(hm_model.defaultParameters().keys(), res.x[0:33])))
  print(params_0[33:])

def optimizeModelExpandingWindow(config, t_begin, t_end, steps):
  params_0 = np.array([p for p in hm_model.defaultParameters().values()])
  params_0 = np.append(params_0, hm_model.defaultInitialConditions())
  
  t_span = t_end - t_begin
  for step in range(1, steps + 1):
    print('NEXT ITERATION: ' + str(step) + '/' + str(steps))
    print('Current parameters')
    print(dict(zip(hm_model.defaultParameters().keys(), params_0[0:33])))
    print(params_0[33:])
    t_end_step = int(t_begin + t_span * (step / steps))
    modelOptFun = hm_opt.getModelOptimizationFunction(config, t_begin, t_end_step)
    res = minimize(modelOptFun, params_0, method='nelder-mead', options={'fatol': 1.0, 'disp': True, 'maxiter' : 250})
    params_0 = res.x

  print(dict(zip(hm_model.defaultParameters().keys(), params_0[0:33])))
  print(params_0[33:])

def main():
  config_path = sys.argv[1]
  with open(config_path, "r") as config_json:
    config = json.load(config_json)
  
  runModel(config, 1632780000, 1644265260)
  # runModel(config, 1642199356 - 45 * 24 * 60 * 60, 1642199356)
  # optimizeModel(config, 1642199356 - 45 * 24 * 60 * 60, 1642199356)
  # optimizeModelExpandingWindow(config, 1642199356 - 45 * 24 * 60 * 60, 1642199356, 10)

if __name__ == "__main__":
  # res = cProfile.run('main()', sort='cumtime')
  res = main()
  exit(res)