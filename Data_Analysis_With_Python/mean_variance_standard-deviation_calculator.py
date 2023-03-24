import numpy as np

def calculate(list):
    # Check if list contains less than 9 elements
    if len(list) < 9:
      raise ValueError("List must contain nine numbers.")

    arr = np.reshape(list, (3, 3))
  
    dict = {}

    # calculating mean
    dict['mean'] = [np.mean(arr, axis=0).tolist(), np.mean(arr, axis=1).tolist(), np.mean(list)]

    # calculating variance
    dict['variance'] = [np.var(arr, axis=0).tolist(), np.var(arr, axis=1).tolist(), np.var(list)]

    # calculating std deviation
    dict['standard deviation'] = [np.std(arr, axis=0).tolist(), np.std(arr, axis=1).tolist(), np.std(list)]

    # calculating max
    dict['max'] = [np.max(arr, axis=0).tolist(), np.max(arr, axis=1).tolist(), np.max(list)]
  
    # calculating min
    dict['min'] = [np.min(arr, axis=0).tolist(), np.min(arr, axis=1).tolist(), np.min(list)]
  
    # calculating sum
    dict['sum'] = [np.sum(arr, axis=0).tolist(), np.sum(arr, axis=1).tolist(), np.sum(list)]
  
    return dict
