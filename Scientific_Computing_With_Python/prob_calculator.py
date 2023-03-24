import copy
from copy import deepcopy
import random
# Consider using the modules imported above.

class Hat:
  def __init__(self, **kwargs):
    self.contents = []
    for k, v in kwargs.items():
      for x in range(v):
        self.contents.append(k)
        
  def draw(self, num):
    result = []
    
    if num > len(self.contents):
      for x in range(len(self.contents)):
        result.append(self.contents[x])
      return result
    
    for x in range(num):
      tempLen = len(self.contents)
      ind = random.randint(0, tempLen-1)
      result.append(self.contents[ind])
      self.contents.pop(ind)
    return result

def printList(l):
  for x in range(len(l)):
    print(x + " ")
    

def experiment(hat, expected_balls, num_balls_drawn, num_experiments):
  success = 0
  
  for x in range(num_experiments):
    temp = copy.deepcopy(hat)
    
    count = dict()
    for k, v in expected_balls.items():
      count[k] = v

    result = temp.draw(num_balls_drawn)
    for s in result:
      if s in count:
        count[s] -= 1

    found = True
    for k, v in count.items():
      if v > 0:
        found = False
        break
    if found:
      success += 1

  print("Sucess: " + str(success))
  print("Total: " + str(num_experiments))
 
  return float(success/num_experiments)