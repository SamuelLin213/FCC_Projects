import math

class Category:
  name = ""
  ledger = []
  balance = 0
  withdraws = 0
  
  def __init__(self, name):
    self.name = name
    self.ledger = []
    self.withdraws = 0
  
  def check_funds(self, amount):
    if amount > self.balance:
      return False
    return True  
  
  def deposit(self, amount, description = ""):
    self.ledger.append({"amount": amount, "description": description})
    self.balance += amount
  
  def withdraw(self, amount, description = ""):
    if not self.check_funds(amount):
      return False

    self.ledger.append({"amount": -1*amount, "description": description})
    self.balance -= amount
    self.withdraws += amount
    
    return True

  def get_balance(self):
    return self.balance

  def transfer(self, amount, account):
    if not self.check_funds(amount):
      return False

    self.balance -= amount
    account.balance += amount
    self.withdraws += amount
    account.ledger.append({"amount": amount, "description": "Transfer from " + self.name})
    self.ledger.append({"amount": -1*amount, "description": "Transfer to " + account.name})
    return True  

  def __str__(self):
    result = self.name.center(30, "*") + "\n"

    for x in self.ledger:
      result += x["description"][0:23].ljust(23) +  str('%.2f' % x["amount"]).rjust(7) + "\n"

    result += "Total: " + str('%.2f' % self.balance)
    
    return result

def create_spend_chart(categories):
  graph = "Percentage spent by category\n"
  maxLen = 0
  
  percents = []
  sum = 0
  for c in categories:
    sum += c.withdraws
  for c in categories:
    temp = int(c.withdraws / sum * 10) * 10
    percents.append(temp)
    if len(c.name) > maxLen:
      maxLen = len(c.name) 
  
  for x in reversed(range(10+1)):
    curr = x*10
    graph += str(curr).rjust(3) + "|"
    for c in range(len(categories)):
      if percents[c] >= curr:
        graph += " o "
      else:
        graph += " " * 3
    graph += " "
    graph += "\n"

  graph += " " * 4

  for x in categories:
    graph += "---"
  graph += "-\n"

  for y in range(maxLen):
    graph += " " * 4
    for c in categories:
      if y >= len(c.name):
        graph += " " * 3
      else:
        graph += " " + c.name[y] + " "
    graph += " "
    graph += "\n"

  graph = graph.rstrip() + " " * 2
    
  return graph