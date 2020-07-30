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
        elif state[0][0] < 21:
            return ['hit', 'stand']
        else:
            return []

    def find_next_state(self, current_state, action):
        if action == 'hit':
            new_card = random.choices([x for x in range(1,11)], [4]*9 + [16], k=1).pop()
            hand = list(current_state[0])
            hand = self.add_new_card(hand, new_card)
            new_state_0 = tuple(hand)

            new_state = (new_state_0,'hit')
        else:
            new_state = current_state[0],'stand'

        hand_value = new_state[0][0]
        if hand_value > 21:
            reward = -1

        else:
            if action == 'stand' or hand_value == 21:
                dealer_hand = self.make_dealer_hand()
                if dealer_hand < hand_value:
                    reward = 1
                elif dealer_hand == hand_value:
                    reward = 0
                else:
                    reward = -1
            else:
                reward = 0

        return new_state, reward

    def start_new_path(self):
        new_cards = random.choices([x for x in range(1,11)], [4]*9 + [16],k=2)
        new_hand = [0] * 2
        for card in new_cards:
            new_hand = self.add_new_card(new_hand, card)
        new_hand = tuple(new_hand),'hit'
        return new_hand

    def make_dealer_hand(self):
        hand = [0]*2
        while hand[0] < 17:
            new_card = random.choices([x for x in range(1,11)], [4]*9 + [16])[0]
            hand = self.add_new_card(hand, new_card)
        total = hand[0]
        if total > 21:
            return 0
        return total

    def add_new_card(self, hand, new_card):
        '''
        Calculates the value of a hand
        here a hand is defined by (total, is ace used as 11)
        '''
        hand_values = list(hand)

        if new_card == 1 and hand_values[1] == 0:
            hand_values[0] += 11
            hand_values[1] = 1
        else:
            hand_values[0] += new_card

        if hand_values[0] > 21 and hand_values[1] == 1:
            hand_values[0] -= 10
            hand_values[1] = 0

        return tuple(hand_values)
