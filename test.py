from strategy import Strategy, Trainer
from game import Left_Right_Game
import random

if __name__ == '__main__':
    game = Left_Right_Game()
    strategy = Strategy(game_graph = {5 : {'left': 1, 'right' : 1}})
    trainer = Trainer(strategy = strategy, current_state = 5, game = game)
    
    #for i in range(1000):
        #print(trainer.current_state)
     #   move = trainer.choose_action(trainer.current_state)
     #   print(move)
     #   if move == 'start_new_path':
     #       trainer.current_state = random.choice(list(strategy.game_graph.keys()))
      #  else:
      #      trainer.update_q_values(trainer.current_state, move)

    trainer.optimize(iterations = 1000)
    print(strategy.game_graph)

