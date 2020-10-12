from strategy import Strategy, Trainer, HumanStrategyTTT
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

def remap_keys(di):
    return [{'key': k, 'value': di[k]} for k in di.keys()]

if __name__ == '__main__':

    game = TicTacToeGame()
    starting_state = game.start_new_path()
    print(starting_state)
    strategy_1 = Strategy(game_graph = {starting_state : {action: 1 for action in game.list_valid_actions(starting_state)}})
    #strategy_2 = Strategy(game_graph = {starting_state :  {action: 1 for action in game.list_valid_actions(starting_state)}})
    strategy_2 = HumanStrategyTTT(game_graph = {starting_state : {action: 1 for action in game.list_valid_actions(starting_state)}})

    trainer = Trainer(players=[strategy_1, strategy_2], current_state=starting_state, game=game,alpha=.1)

    trainer.optimize(iterations=500,stupid_periods=4)

    with open('results_{}.json'.format(datetime.now().strftime('%y-%m-%d')), 'w') as file:
        file.write(str(strategy_1.game_graph))

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

