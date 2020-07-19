import random
import math

def softmax_clipped(vals):
    exp_vals = [math.exp(min(100, val)) for val in vals]
    total_exp = sum(exp_vals)
    return [val / total_exp for val in exp_vals]

class Strategy:
    def __init__(self, game_graph = {}):
        self.game_graph = game_graph

class Trainer:
    def __init__(self, strategy, current_state, game,alpha = 1, gamma = 0.1):
        self.alpha = alpha
        self.gamma = gamma
        self.strategy = strategy
        self.current_state = current_state
        self.game = game

    def make_move(self, old_state, action):
        new_state, reward = self.game.find_next_state(old_state, action)
        if new_state not in self.strategy.game_graph:
            valid_actions = self.game.list_valid_actions(new_state)
            if valid_actions is None:
                self.strategy.game_graph[new_state] = {}
            else:
                self.strategy.game_graph[new_state] = dict(zip(valid_actions, [1]*len(valid_actions)))
        self.current_state = new_state
        return new_state, reward

    def update_q_values(self, old_state, action):
        old_q = self.strategy.game_graph[old_state][action]
        new_state, reward = self.make_move(old_state, action)
        new_state_actions = self.strategy.game_graph[new_state].keys()
        new_q_vals = [self.strategy.game_graph[new_state][action] for action in new_state_actions] 
        max_q = max(new_q_vals, default = 0)

        new_q = old_q + self.alpha*(reward + self.gamma*max_q - old_q)
        self.strategy.game_graph[old_state][action] = new_q

    def choose_action(self, current_state):
        new_path = False
        possible_moves = list(self.strategy.game_graph[current_state].keys())
        if len(possible_moves) == 0:
            action = 'start_new_path'
        else:
            q_vals = [self.strategy.game_graph[current_state][action] for action in possible_moves]
            weights = softmax_clipped(q_vals)
            action = random.choices(possible_moves, weights = weights)[0]
        return action

    def optimize(self, iterations = 100):
        for i in range(iterations):
            move = self.choose_action(self.current_state)
            if move == 'start_new_path':
                self.current_state = random.choice(list(self.strategy.game_graph.keys()))
            else:
                self.update_q_values(self.current_state, move)
