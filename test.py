from strategy import Strategy, Trainer
from game import Left_Right_Game, BlackJack, TicTacToeGame
import json
import pickle
from datetime import datetime

import random

def decode(x):
    try:
        return x.decode()
    except:
        return x

# if __name__ == '__main__':
#     game = Left_Right_Game()
#     strategy = Strategy(game_graph = {5 : {'left': 1, 'right' : 1}})
#     trainer = Trainer(strategy = strategy, current_state = 5, game = game)
#
#     #for i in range(1000):
#         #print(trainer.current_state)
#      #   move = trainer.choose_action(trainer.current_state)
#      #   print(move)
#      #   if move == 'start_new_path':
#      #       trainer.current_state = random.choice(list(strategy.game_graph.keys()))
#       #  else:
#       #      trainer.update_q_values(trainer.current_state, move)
#
#     trainer.optimize(iterations = 1000)
#     print(strategy.game_graph)

if __name__ == '__main__':

    game = TicTacToeGame()
    starting_state = game.start_new_path()
    print(starting_state)
    strategy_1 = Strategy(game_graph = {starting_state : {action: 1 for action in game.list_valid_actions(starting_state)}})
    strategy_2 = Strategy(game_graph = {starting_state :  {action: 1 for action in game.list_valid_actions(starting_state)}})

    trainer = Trainer(players=[strategy_1, strategy_2], current_state=starting_state, game=game,alpha=.1)

    trainer.optimize(iterations=500,stupid_periods=4)


    strategy_new = {key: strategy_1.game_graph[key].bytes() for key in strategy_1.game_graph.keys()}
    # json_thing = json.dumps(strategy_new)
    with open('results_{}.json'.format(datetime.now().strftime('%y-%m-%d')), 'wb') as file:
        json.dump(strategy_new,file)

    keys = list(strategy_1.game_graph.keys())
    try:
        keys.sort()
    except:
        pass
    for key in keys:
        if len(strategy_1.game_graph[key]) > 0:
            game.pretty_print_board(key)

            print(strategy_1.game_graph[key])
            print('*******************************************************************')
            print('*******************************************************************')


print('complete')

