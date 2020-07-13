from tictactoe import TicTacToeGame
import ast
from draw_board import draw_board
import matplotlib.pyplot as plt

if __name__ == '__main__':
    tt = TicTacToeGame()

    winner = None
    players = ['x', 'o']
    current_player = 1

    draw_board(tt.board)
    
    while winner is None:
        current_player = 1 - current_player

        position = input('Input {}\'s move: '.format(players[current_player]))
        position = ast.literal_eval(position)

        tt.make_move(player = players[current_player], position = position)
        
        # Close the old plot
        plt.close()
        draw_board(tt.board)

        winner = tt.check_for_winner()
        
    print('{} wins'.format(players[current_player]))
    # Keep final plot open until pressing enter
    input('Press Enter to exit.')
