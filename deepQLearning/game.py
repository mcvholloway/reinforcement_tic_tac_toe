import numpy as np
import random
import logging

logging.basicConfig(level=logging.DEBUG)

class ConnectFourGame():
    def __init__(self, opponent = None):
        self.shape = (6,7)
        self.board = np.zeros(shape=self.shape)
        self.n = 7
        self.opponent = opponent

    def reset(self):
        self.board = np.zeros(shape=self.shape)
        return self.board


    def check_for_winner(self, board):
        board = np.array(board)
        # first, check the rows
        for i in range(6):
            for j in range(4):
                if abs(board[i, j:j + 4].sum()) == 4:
                    return True
        # then, check the columns
        for i in range(3):
            for j in range(7):
                if abs(board[i:i + 4, j].sum()) == 4:
                    return True
        # then, diagonals
        for i in range(3):
            for j in range(4):
                if abs(sum([board[i + k, j + k] for k in range(4)])) == 4:
                    return True
                if abs(sum([board[i + 3 - k, j + k] for k in range(4)])) == 4:
                    return True
        return False

    def start_new_path(self):
        board = np.zeros(shape=(6, 7))
        board = tuple(map(tuple, board))
        return board

    def list_valid_actions(self, state):
        state = np.array(state)

        if self.check_for_winner(state):
            return []

        # find the columns that have at least one empty space
        return [x for x in range(7) if np.abs(state[:, x]).sum() < 6]


    def update_board(self, action):
        stale_mate = False
        game_over = False
        board_sum = self.board.sum().sum()

        ### super genius! If board sum is 0, want it to be 1's turn,
        ### else if board sum is 1, want it to be -1's turn!
        next_player = (-1) ** board_sum

        # figure out where to place the new piece by extracting that column out
        col = self.board[:, action]
        new_spot = len(col[col == 0]) - 1

        self.board[new_spot, action] = next_player

        if self.check_for_winner(self.board):
            reward = 1
            game_over = True
            stale_mate = False
        elif np.abs(self.board).sum() == 6 * 7:
            reward = -1
            game_over = True
            stale_mate = True
        else:
            reward = 0

        return reward, game_over

    def model_makes_move(self, model):
        return np.argmax(model.predict(self.board.reshape(1,42)))

    def step(self, action):
        outcome = self.update_board(action)
        if outcome[1]:
            return self.board, outcome[0], True, None
        if self.opponent:
            computer_move = self.model_makes_move(self.opponent)
        else:
            computer_move = random.choice(self.list_valid_actions(self.board))
        outcome = self.update_board(computer_move)

        if -np.abs(outcome[0]) == -1:
            logging.debug('######################################################')
            logging.debug('I beat you by using an inferior AI, you sorry sack of shit!!!!')
        return self.board, -np.abs(outcome[0]), outcome[1], None

    def check_for_terminal(self, state):
        current_state = np.array(state)

        if self.check_for_winner(current_state):
            return 1
        if np.abs(current_state).sum() == 6 * 7:
            return 1
        return 0

    def calculate_reward(self, state):
        current_state = np.array(state)

        if self.check_for_winner(current_state):
            return 2
        if np.abs(current_state).sum() == 6 * 7:
            return 0
        return 0

    def pretty_print_board(self, board):

        board = np.array(board)
        symbol_lookup = {-1: 'o', 1: 'x', 0: ' '}

        middle_row = ['-', '+', '-', '+', '-', '+', '-', '+', '-', '+', '-', '+', '-']

        def pad_row(row):
            return [symbol_lookup[row[0]],
                    '|',
                    symbol_lookup[row[1]],
                    '|',
                    symbol_lookup[row[2]],
                    '|',
                    symbol_lookup[row[3]],
                    '|',
                    symbol_lookup[row[4]],
                    '|',
                    symbol_lookup[row[5]],
                    '|',
                    symbol_lookup[row[6]]
                    ]

        nice_board = [pad_row(board[0]),
                      middle_row,
                      pad_row(board[1]),
                      middle_row,
                      pad_row(board[2]),
                      middle_row,
                      pad_row(board[3]),
                      middle_row,
                      pad_row(board[4]),
                      middle_row,
                      pad_row(board[5])
                      ]
        for row in nice_board:
            print(*row)

