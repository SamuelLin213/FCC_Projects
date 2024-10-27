import re

def arithmetic_arranger(problems, ans = False):
  if len(problems) > 5:
    return "Error: Too many problems."

  operand1 = []
  operand2 = []
  operators = []
  lengths = []
  answers = []
  
  for prob in problems:
    if re.findall("[a-zA-z]", prob):
      return "Error: Numbers must only contain digits."
    
    nums = re.findall("\d+", prob)
    num1 = nums[0]
    num2 = nums[1]

    op = re.findall("\s(\+|-)\s", prob)
    if op:
      numLen = max(len(str(num1)), len(str(num2)) )
      if numLen > 4:
        return "Error: Numbers cannot be more than four digits."
      
      maxLen = numLen + 1
      operand1.append(num1)
      operand2.append(num2)
      operators.append(op[0])
      lengths.append(maxLen)

      if op[0] == '+':
        answers.append(str(int(num1) + int(num2)))
      else:
        answers.append(str(int(num1) - int(num2)))
      
    else:
      return "Error: Operator must be '+' or '-'."      
  
  arranged_problems = ""
  for x in range(len(problems)):
    temp = operand1[x]
    while len(temp) != lengths[x]+1:
      temp = " " + temp
    arranged_problems += temp
    if x == len(problems)-1:
      break
    arranged_problems += "    "
  arranged_problems += "\n"

  for x in range(len(problems)):
    tempOp = operators[x]
    temp = operand2[x]

    while len(temp) != lengths[x]:
      temp = " " + temp
    arranged_problems += tempOp + temp
    if x == len(problems)-1:
      break
    arranged_problems += "    "
  arranged_problems += "\n"

  for x in range(len(problems)):
    temp = ""
    for y in range(lengths[x]+1):
      temp += "-"
    arranged_problems += temp
    if x == len(problems)-1:
      break
    arranged_problems += "    "

  if ans == True:
    arranged_problems += "\n"
    for x in range(len(problems)):
      temp = answers[x]
      while len(temp) < lengths[x]+1:
        temp = " " + temp
      arranged_problems += temp

      if x == len(problems)-1:
        break
      arranged_problems += "    "
  
  return arranged_problems