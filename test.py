from strategy import Strategy, Trainer, HumanStrategyTTT, HumanStrategyC4, MCTSStrategy
from game import Left_Right_Game, BlackJack, TicTacToeGame, ConnectFourGame
import json
import pickle
from datetime import datetime
import ast
import numpy as np

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
    #game = ConnectFourGame()
    starting_state = game.start_new_path()
    #strategy_1 = Strategy(game_graph = {starting_state : {action: 1 for action in game.list_valid_actions(starting_state)}})
    strategy_2 = MCTSStrategy(game = game, game_graph = {starting_state: [0]})
    #strategy_2 = Strategy(game_graph = {starting_state :  {action: 1 for action in game.list_valid_actions(starting_state)}})
    
    #with open('results_20201011-232814.json', 'r') as fi:
    #with open('c4_results_20201012-224658.json', 'r') as fi:
    #with open('ttt_results_20201013-090803.json', 'r') as fi:
    #    res = fi.read()
    #res = ast.literal_eval(res)

    #strategy_1 = Strategy(game_graph = res)
    strategy_1 = HumanStrategyTTT(game_graph = {starting_state : {action: 1 for action in game.list_valid_actions(starting_state)}})
    #strategy_2 = HumanStrategyC4(game_graph = {starting_state : {action: 1 for action in game.list_valid_actions(starting_state)}})


    trainer = Trainer(players=[strategy_1, strategy_2], current_state=starting_state, game=game,alpha=.1)
    #trainer = Trainer(players=[strategy_1, strategy_1], current_state=starting_state, game=game,alpha=.1)


    trainer.optimize(iterations=1000,stupid_periods=-1)
    #trainer.optimize(iterations=10000000,stupid_periods=10)

    with open('ttt_results_{}.json'.format(datetime.now().strftime('%Y%m%d-%H%M%S')), 'w') as file:
        file.write(str(strategy_1.game_graph))

    # keys = list(strategy_1.game_graph.keys())
    # try:
    #     keys.sort()
    # except:
    #     pass
    # for key in keys:
    #     if len(strategy_1.game_graph[key]) > 0:
    #         game.pretty_print_board(key)
    #         if np.array(key).sum() == 0:
    #             print('X\'s Turn')
    #         else:
    #             print('O\'s Turn')
    #         #print(key)

    #         print(strategy_1.game_graph[key])
    #         print('*******************************************************************')
    #         print('*******************************************************************')


print('complete')

