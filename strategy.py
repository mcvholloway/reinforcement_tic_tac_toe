import random
import math
import logging

logging.basicConfig(level=logging.INFO)


def softmax_clipped(vals: list) -> list:
    """Takes in list of floats and returns probabilies associated to actions"""

    ### Clip Values to Avoid overflow in latter step
    vals = [min(100, val) for val in vals]

    exp_vals = [math.exp(val) for val in vals]
    total_exp = sum(exp_vals)
    return [val / total_exp for val in exp_vals]

class Strategy:
    ### TODO Add MCTS Update values
    """Class that initiates game graph and provides a method, depending on strategy type, to update
    the values that dictates the decisions of the player """

    def __init__(self, game_graph = {}, strategy_type = "q_learning"):

        ### game_graph is a dictionary of dictionaries -- keys are states
        ### and keys of keys are actions and values are q-values
        self.game_graph = game_graph

    def update_q_values(self, old_state, action, alpha, gamma, new_state, reward):

        old_q = self.game_graph[old_state][action]
        # new_state, reward = self.make_move(old_state, action)
        new_state_actions = self.game_graph[new_state].keys()
        new_q_vals = [self.game_graph[new_state][action] for action in new_state_actions]
        max_q = max(new_q_vals, default=0)

        new_q = old_q + alpha * (reward + gamma * max_q - old_q)
        self.game_graph[old_state][action] = new_q

    def choose_action(self, current_state, stupidity_rate=0):

        possible_moves = list(self.game_graph[current_state].keys())
        if len(possible_moves) == 0:
            action = 'start_new_path'
        else:
            being_stupid = random.choices([['yes', 'no'], [stupidity_rate, 1 - stupidity_rate]], k=1).pop()
            if being_stupid == 'no':
                q_vals = [self.game_graph[current_state][action] for action in possible_moves]
                weights = softmax_clipped(q_vals)
                action = random.choices(possible_moves, weights=weights)[0]
            else:
                action = random.choice(possible_moves)
        return action

class Trainer:
    def __init__(self, players, current_state, game,alpha = 1, gamma = 0.1, stupidity_rate=0):
        if not isinstance(players,list):
            players = [players]
        self.alpha = alpha
        self.gamma = gamma
        self.current_state = current_state
        self.game = game
        self.current_turn = 0
        self.players = players
        self.strategy = players[self.current_turn]
        self.number_players = len(self.players)
        # self.stalemate = g


    def make_move(self, old_state, action):
        new_state, reward, game_over,stale_mate = self.game.find_next_state(old_state, action)
        if new_state not in self.strategy.game_graph:
            valid_actions = self.game.list_valid_actions(new_state)
            if valid_actions is None:
                self.strategy.game_graph[new_state] = {}
            else:
                self.strategy.game_graph[new_state] = dict(zip(valid_actions, [1]*len(valid_actions)))
        self.current_state = new_state
        return new_state, reward, game_over, stale_mate



    def optimize(self, iterations = 100):
        ### backlog keys are players and values are (state when move was made, action)
        backlog = {}
        for i in range(iterations):
            if i % 10000 == 0:
                logging.info(str(i))
            if self.strategy in backlog:

                old_state,move = backlog.pop(self.strategy)
                ### since player is making future move, no reward at the moment......
                self.strategy.update_q_values(old_state =old_state,
                                              action=move,
                                              alpha =self.alpha,
                                              gamma=self.gamma,
                                              new_state=self.current_state,
                                              reward=0)

            stupidity_rate = math.cos((math.pi/2)*(i/iterations))**2
            move = self.strategy.choose_action(self.current_state,stupidity_rate=stupidity_rate)


            if move == 'start_new_path':
                # self.current_state = random.choice(list(self.strategy.game_graph.keys()))
                self.current_state = self.game.start_new_path()
                if self.current_state not in self.strategy.game_graph:
                    valid_actions = self.game.list_valid_actions(self.current_state)
                    self.strategy.game_graph[self.current_state] = dict(zip(valid_actions, [1] * len(valid_actions)))

            else:

                ### Log Activity
                backlog[self.strategy] = (self.current_state, move)
                new_state, reward, game_over, stale_mate = self.game.find_next_state(self.current_state, move )


                ### update current state
                self.current_state = new_state
                if game_over:
                    old_state, move = backlog.pop(self.strategy)
                    if new_state not in self.strategy.game_graph:
                        valid_actions = self.game.list_valid_actions(new_state)
                        if valid_actions is None:
                            self.strategy.game_graph[new_state] = {}
                        else:
                            self.strategy.game_graph[new_state] = dict(zip(valid_actions, [1] * len(valid_actions)))
                    ### since player is making future move, no reward at the moment......
                    self.strategy.update_q_values(old_state=old_state,
                                                  action=move,
                                                  alpha=self.alpha,
                                                  gamma=self.gamma,
                                                  new_state=self.current_state,
                                                  reward=reward)


                    if not stale_mate:
                        reward = -reward

                    for log in backlog.keys():
                        old_state, move = backlog[log]
                        if new_state not in log.game_graph:
                            valid_actions = self.game.list_valid_actions(new_state)
                            if valid_actions is None:
                                log.game_graph[new_state] = {}
                            else:
                                log.game_graph[new_state] = dict(zip(valid_actions, [1] * len(valid_actions)))
                        log.update_q_values(old_state=old_state,
                                                      action=move,
                                                      alpha=self.alpha,
                                                      gamma=self.gamma,
                                                      new_state=self.current_state,
                                                      reward=reward)

                    ### Game ended so start new iteration
                    backlog = {}
                    continue


                else:
                    ### Switch to next player
                    self.strategy = self.players[(self.current_turn + 1) % self.number_players]

                    if new_state not in self.strategy.game_graph:
                        valid_actions = self.game.list_valid_actions(new_state)
                        if valid_actions is None:
                            self.strategy.game_graph[new_state] = {}
                        else:
                            self.strategy.game_graph[new_state] = dict(zip(valid_actions, [1] * len(valid_actions)))
                    self.current_state = new_state















    # def update_q_values(self, old_state, action):
    #     old_q = self.strategy.game_graph[old_state][action]
    #     new_state, reward = self.make_move(old_state, action)
    #     new_state_actions = self.strategy.game_graph[new_state].keys()
    #     new_q_vals = [self.strategy.game_graph[new_state][action] for action in new_state_actions]
    #     max_q = max(new_q_vals, default = 0)
    #
    #     new_q = old_q + self.alpha*(reward + self.gamma*max_q - old_q)
    #     self.strategy.game_graph[old_state][action] = new_q
    #
    # def choose_action(self, current_state,stupidity_rate=0):
    #     new_path = False
    #     possible_moves = list(self.strategy.game_graph[current_state].keys())
    #     if len(possible_moves) == 0:
    #         action = 'start_new_path'
    #     else:
    #         being_stupid = random.choices([['yes','no'], [stupidity_rate, 1 - stupidity_rate]],k=1).pop()
    #         if being_stupid == 'no':
    #             q_vals = [self.strategy.game_graph[current_state][action] for action in possible_moves]
    #             weights = softmax_clipped(q_vals)
    #             action = random.choices(possible_moves, weights = weights)[0]
    #         else:
    #             action = random.choice(possible_moves)
    #     return action