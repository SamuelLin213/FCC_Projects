def add_time(start, duration, day = None):
  colon = start.find(':')
  nextDay = False
  numDays = 0
  
  startH = int(start[0:colon])
  startM = int(start[colon+1:colon+3])

  time = start[-2:]
  
  colon = duration.find(':')
  durH = int(duration[0:colon])
  durM = int(duration[colon+1:colon+3])

  newH = startH + durH
  newM = startM + durM

  while newM >= 60:
    newM -= 60
    newH += 1
  while newH >= 12:
    newH -= 12
    if time == "PM":
      time = "AM"
      nextDay = True
      numDays+=1
    else:
      time = "PM"

  if newH == 0:
    newH = 12
  
  result = str(newH) + ":"
  if newM < 10:
    result += "0" + str(newM)
  else:
    result += str(newM)

  result += " " + time
  
  if day != None:
      days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
  
      ind = days.index(day.lower()) + numDays
      while ind > len(days)-1:
        ind -= (len(days))
      result += ", " + days[ind][0:1].upper() + days[ind][1:]

  if numDays > 1:
    result += " (" + str(numDays) + " days later)"
    
  if nextDay and numDays == 1:
    result += " (next day)"
    
  return result
