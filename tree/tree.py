import random

class Tree:
    def __init__(self, directory = {}):
        self.directory = directory

class RandomGame:
    def __init__(self):
        pass
    
    def find_next_state(self, state, action):
        return random.randint(1, 3)

    def find_actions(self, state):
        return ['left', 'right']

    def check_for_terminal(self, state):
        return random.choice([0,1])

class Node:
    def __init__(self, address, tree, game, current_state, parent = None):
        self.parent = parent
        self.game = game
        self.tree = tree
        self.current_state = current_state
        actions = self.game.list_valid_actions(current_state)
        di = {}
        for action in actions:
            di[action] = [0,0]
        self.actions = di
        self.address = address
        tree.directory[address] = self
        self.terminal = game.check_for_terminal(current_state)

    def make_child(self, action):
        next_state = self.game.find_next_state(self.current_state, action)
        new_address = self.address + (action, next_state)
        if new_address not in self.tree.directory:
            Node(address = new_address, game = self.game, tree = self.tree, parent = self, current_state = next_state)
        return new_address


