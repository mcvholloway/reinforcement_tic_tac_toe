import random

class Left_Right_Game:
    def __init__(self):
        pass

    def list_valid_actions(self, state):
        if state == 0:
            return ['right']
        elif state == 10:
            pass
        else: 
            return ['right', 'left']

    def find_next_state(self, current_state, action):
        if action == 'left':
            new_state = current_state - 1
        else:
            new_state = current_state + 1

        if new_state == 10:
            reward = 100
        else:
            reward = 0

        return new_state, reward


class BlackJack:
    def __init__(self):
        pass


    def list_valid_actions(self, state):
        if state[1] == 'stand':
            return []
        elif state[0] < 21:
            return ['hit', 'stand']
        else:
            return []

    def find_next_state(self, current_state, action):
        if action == 'hit':
            new_state_0 = current_state[0] + random.choices([x for x in range(2,11)], [4]*8 + [16], k=1).pop()
            new_state_1 = current_state[1]
            new_state = (new_state_0,new_state_1)
        else:
            new_state = current_state[0],'stand'

        if new_state[0] > 21:
            reward = -1000

        else:
            if action == 'stand':
                reward = (current_state[0] - 21)**3
            elif new_state[0] == 21:
                reward = 10000
            else:
                reward = 0

        return new_state, reward

    def start_new_path(self):
        new_cards = random.choices([x for x in range(2,11)], [4]*8 + [16],k=2)
        new_hand = sum(new_cards),'hit'
        return new_hand
