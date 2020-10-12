from game import BlackJack
from tree import Tree
from tree import Node
import random

if __name__ == '__main__':
    game = BlackJack()
    tree = Tree()
    #starting_state = game.start_new_path()
    starting_state = ((20,0), 'hit', 6)
    node = Node(address = (starting_state,), tree = tree, game = game, current_state = starting_state)

    for _ in range(100):
    
        while not node.terminal:
            action = random.choice(list(node.actions.keys()))
            node.actions[action][1] += 1
            node = tree.directory[node.make_child(action)]

        reward = game.calculate_reward(node.current_state)

        while node.parent:
            action = node.address[-2]
            node = node.parent
            node.actions[action][0] += reward
    
    print(starting_state)
    print(tree.directory[(starting_state,)].actions)

