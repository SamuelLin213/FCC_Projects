# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.

def player(prev_opponent_play,
          opponent_history=[],
          play_order={}):
  # first move; set default to 'R'
  if not prev_opponent_play:
    prev_opponent_play = 'R'
  opponent_history.append(prev_opponent_play)  # adds previous move to history

  # store moves to look back to
  num = 6
            
  # gets last three moves of opponent
  lastMoves = "".join(opponent_history[-num:])
  if len(opponent_history) > num: # enough previous moves for num
    if "".join(opponent_history[-(num+1):]) in play_order:
      play_order["".join(opponent_history[-(num+1):])] += 1
    else:
      play_order["".join(opponent_history[-(num+1):])] = 1

  # Creates pairs of 3, using opponent's previous move
  potential_plays = [
    lastMoves + "R",
    lastMoves + "P",
    lastMoves + "S"
  ]

  for x in potential_plays:
    if not x in play_order:
      play_order[x] = 0

  # Creates array of count from play order
  sub_order = {
    k: play_order[k]
    for k in potential_plays if k in play_order
  }

  # predicts opponent's next move
  prediction = max(sub_order, key=sub_order.get)[-1:]
            
  # mapping of counter to moves
  ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
  return ideal_response[prediction]