from scipy.optimize import minimize
from scipy import optimize
import numpy as np
from datetime import datetime
import pytz
import sys
import json
import cProfile

# heat model modules
import hm_db
import hm_model
import hm_opt

def runModel(config, t_begin, t_end):
  model = hm_model.Model.fromOptParameters(hm_model.defaultParameters())
  x_0 = hm_model.defaultInitialConditions().T[0]
  t_space, dt_space = hm_model.prepareTime(t_begin, t_end)
  ub = hm_db.retrieveExternalConditions(config['influx-db-config'], t_begin, t_end)
  # import code
  # code.interact(local=locals())
  solution = model.run(t_space, x_0, ub)
  solution.dt_space = dt_space
  # print('x1 error: ' + str(computeError(x12['x1'], x1_num_sol)))
  # print('x2 error: ' + str(computeError(x12['x2'], x2_num_sol)))
  x12 = hm_db.retrieveKnownStates(config['influx-db-config'], t_begin, t_end)
  hm_model.visualizeRun(solution, [x12['x1'], x12['x2']])

def optimizeModel(config, t_begin, t_end):
  params_0 = hm_model.defaultParameters()
  params_0 = np.append(params_0, hm_model.defaultInitialConditions())
  modelOptFun = hm_opt.getModelOptimizationFunction(config, t_begin, t_end)
  res = minimize(modelOptFun, params_0, method='nelder-mead', options={'xatol': 1e+2, 'disp': True, 'maxiter' : 10000})
  # res = minimize(modelOptFun, params_0, method='trust-constr', bounds=hm_model.bounds())
  # res = optimize.shgo(modelOptFun, hm_model.bounds())
  print(res)

def main():
  config_path = sys.argv[1]
  with open(config_path, "r") as config_json:
    config = json.load(config_json)
  
  # runModel(config, 1642199356 - 35 * 24 * 60 * 60, 1642199356)
  optimizeModel(config, 1642199356 - 35 * 24 * 60 * 60, 1642199356)

if __name__ == "__main__":
  # res = cProfile.run('main()', sort='cumtime')
  res = main()
  exit(res)