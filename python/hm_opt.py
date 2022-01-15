import hm_db
import hm_model
import numpy as np
from scipy.integrate import solve_ivp
import pandas as pd
from datetime import datetime
import pytz

def computeError(reference, results):
  return sum(pow(reference - results, 2))

def getModelOptimizationFunction(config, t_begin, t_end):
  
  ub = hm_db.retrieveExternalConditions(config['influx-db-config'], t_begin, t_end)
  x12 = hm_db.retrieveKnownStates(config['influx-db-config'], t_begin, t_end)

  t_space, dt_space = hm_model.prepareTime(t_begin, t_end)
  # import code
  # code.interact(local=locals())  
  # ub = ub[0::10]
  # x1 = x12['x1'][0::10]
  # x2 = x12['x2'][0::10]
  # t_space = t_space[0::10]
  # dt_space = dt_space[0::10]
  # import code
  # code.interact(local=locals())  
  def modelOptimizationFunction(params):
    print('params: ' + str(params))
    x_0 = params[31:]

    model = hm_model.Model.fromOptParameters(params[0:31])

    solution = model.run(t_space, x_0, ub)
    X_num_sol = solution.y
    x1_num_sol = pd.Series(X_num_sol[0].T, index=dt_space)
    x2_num_sol = pd.Series(X_num_sol[1].T, index=dt_space)
    
    error = computeError(x12['x1'], x1_num_sol) + computeError(x12['x2'], x2_num_sol)
    # error = computeError(x1, x1_num_sol) + computeError(x2, x2_num_sol)
    print('error: ' + str(error))
    return error
    
  return modelOptimizationFunction