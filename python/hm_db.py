from influxdb import InfluxDBClient
import pandas as pd

# TODO that should not be here, it calibration should be done by the user, not in retrieveing
def defaultCoveredSensorLuxCalibration():
  return lambda m : 15000000.0 / ( 2550000.0 / m - 10000)
  
def defaultUncoveredSensorLuxCalibration():
  return lambda m : 5000000.0 / ( 2550000.0 / m - 10000)

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
