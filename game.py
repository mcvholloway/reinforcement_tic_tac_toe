import random
import numpy as np
import itertools



class TicTacToeGame():
    def __init__(self):
        self.board = np.zeros(shape=(3, 3))

    def make_move(self, player, position):
        '''
        player: 'x' or 'o'
        position: tuple

        Takes a player and position, checks that the position is open
        and then updates the board
        '''

        x, y = position
        if self.board[x][y] == 0:
            if player == 'x':
                self.board[x][y] = 1
            elif player == 'o':
                self.board[x][y] = -1

    def check_for_winner(self):
        '''
        Checks all possible ways to win and returns the winning player
        If no winning player, returns nothing
        '''

        for i in range(3):
            # First check the rows
            if sum(self.board[i]) == 3:
                return 'x'
            if sum(self.board[i]) == -3:
                return 'o'
            # Then check the columns
            if sum([row[i] for row in self.board]) == 3:
                return 'x'
            if sum([row[i] for row in self.board]) == -3:
                return 'o'

        # Then check the diagonals
        if sum([self.board[i][i] for i in range(3)]) == 3:
            return 'x'
        if sum([self.board[i][i] for i in range(3)]) == -3:
            return 'o'
        if sum([self.board[i][2 - i] for i in range(3)]) == 3:
            return 'x'
        if sum([self.board[i][2 - i] for i in range(3)]) == -3:
            return 'o'

    def check_for_tie(self):
        lines_dict = dict()
        for i in range(3):
            row_list = []
            for j in range(3):
                row_list.append(self.board[i][j])
            lines_dict.update({'row_{}'.format(str(i)): set(row_list)})
        for i in range(3):
            column_list = []
            for j in range(3):
                column_list.append(self.board[j][i])
            lines_dict.update({'column_{}'.format(str(i)): set(column_list)})
        up_right = []
        down_left = []
        for i in range(3):
            up_right.append(self.board[i][i])
            down_left.append(self.board[i][2 - i])
        lines_dict.update({'up_right': set(up_right), 'down_lef': set(down_left)})
        lines_left = []
        for line in lines_dict.keys():
            if {1, -1}.issubset(lines_dict[line]):
                pass
            else:
                lines_left.append(line)
        if lines_left == []:
            return 'TieGame'

    def pretty_print_board(self, board):

        board = np.array(board)
        symbol_lookup = {-1: 'o', 1: 'x', 0: ' '}

        middle_row = ['-', '+', '-', '+', '-']

        def pad_row(row):
            return [symbol_lookup[row[0]],
                    '|',
                    symbol_lookup[row[1]],
                    '|',
                    symbol_lookup[row[2]]]

        nice_board = [pad_row(board[0]),
                      middle_row,
                      pad_row(board[1]),
                      middle_row,
                      pad_row(board[2])]
        for row in nice_board:
            print(*row)

    def start_new_path(self):
        board = np.zeros(shape=(3,3))
        board = tuple(map(tuple, board))
        return board

    def list_valid_actions(self,state):
        state = np.array(state)

        if np.abs(state.sum(axis=0)).max() == 3 or \
                np.abs(state.sum(axis=1)).max() == 3  or \
                abs(sum([state[i,i] for i in range(3)])) == 3 or \
                abs(sum([state[i, 2 - i] for i in range(3)])) == 3:
            return []

        return [x for x in list(itertools.product(*[[0,1,2], [0,1,2]])) if state[x] == 0]


    def find_next_state(self, current_state, action):

        current_state = np.array(current_state)
        stale_mate = False
        game_over = False
        board_sum = current_state.sum().sum()

        ### super genius! If board sum is 0, want it to be 1's turn,
        ### else if board sum is 1, want it to be -1's turn!
        next_player = (-1)**board_sum

        current_state[action] = next_player

        if np.abs(current_state.sum(axis=0)).max() == 3 or \
                np.abs(current_state.sum(axis=1)).max() == 3  or \
                abs(sum([current_state[i,i] for i in range(3)])) == 3 or \
                abs(sum([current_state[i, 2 - i] for i in range(3)])) == 3:
            reward = 1
            game_over = True
            stale_mate = False
        elif np.abs(current_state).sum() == 9:
            reward = -1
            game_over = True
            stale_mate = True
        else:
            reward = 0
        
        new_state = tuple(map(tuple, current_state))

        return new_state, reward, game_over, stale_mate








class Chess:
    def __init__(self):
        ### for logging
        self.piece_dictionary = {
            'p': 'pawn',
            'q': 'queen',
            'k': 'king',
            'b': 'bishop',
            'h': 'knight', # h for horse
            'r': 'rook',
        }
        self.board = [[None]*8]*8

        ### pieces keeps track of pieces each player has
        self.pieces = {'white': [],
                       'black': []
                       }

    def start_new_path(self):

        for i in range(8):
            self.board[7][i] = ('p','w')
            self.board[2][i] = ('p','b')

        for i in [(0,'w'), (8,'b')]:

            self.board[i][0] = ('r', i[1])
            self.board[i][7] = ('r', i[1])

            self.board[i][6] = ('h', i[1])
            self.board[i][1] = ('h', i[1])

            self.board[i][5] = ('b', i[1])
            self.board[i][2] = ('b', i[1])

            self.board[i][4] = ('k', i[1])

            self.board[i][3] = ('q', i[1])

        return self.board

    def list_valid_actions(self):
        return None

    def find_next_state(self, current_state, action):
        return None



class Left_Right_Game:
    def __init__(self):
        pass

    def start_new_path(self):
        return random.randint(1,8)

    def list_valid_actions(self, state):
        if state == 0:
            return ['right']
        elif state == 10:
            pass
        else: 
            return ['right', 'left']

    def find_next_state(self, current_state, action):

        stale_mate = False
        if action == 'left':
            new_state = current_state - 1
        else:
            new_state = current_state + 1

        if new_state == 10:
            reward = 100
            game_over = True
        else:
            reward = 0
            game_over = False

        return new_state, reward, game_over, stale_mate


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

            new_state = (new_state_0,'hit',current_state[2])
        else:
            new_state = current_state[0],'stand',current_state[2]

        hand_value = new_state[0][0]
        if hand_value > 21:
            reward = -1
            game_over = True

        else:
            if action == 'stand' or hand_value == 21:
                game_over = True

                dealer_hand = self.make_dealer_hand(current_state[2])
                if dealer_hand < hand_value:
                    reward = 1
                elif dealer_hand == hand_value:
                    reward = 0
                else:
                    reward = -1
            else:
                game_over = False
                reward = 0

        return new_state, reward, game_over, False

    def start_new_path(self):
        dealer_card = random.choices([x for x in range(1,11)], [4]*9 + [16],k=1).pop()
        new_cards = random.choices([x for x in range(1,11)], [4]*9 + [16],k=2)
        new_hand = [0] * 2
        for card in new_cards:
            new_hand = self.add_new_card(new_hand, card)
        new_hand = tuple(new_hand),'hit', dealer_card
        return new_hand

    ### TODO Add hitting on Soft 17 for dealer
    ### TODO Add Split Functionality
    ### TODO Add Double Down Functionality
    ### TODO Add Surender Option
    ### TODO Add Insurance
    ### TODO DISPLAY

    def make_dealer_hand(self, showing_card):
        hand = [0]*2
        hand = self.add_new_card(hand, showing_card)
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
