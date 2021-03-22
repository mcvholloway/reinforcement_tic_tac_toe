from tictactoe import TicTacToeGame
import ast
from draw_board import draw_board
import matplotlib.pyplot as plt

if __name__ == '__main__':
    tt = TicTacToeGame()
    tie = None
    winner = None
    players = ['x', 'o']
    current_player = 1

    draw_board(tt.board)
    
    while winner is None and tie is None:
        current_player = 1 - current_player

        position = input('Input {}\'s move: '.format(players[current_player]))
        position = ast.literal_eval(position)

        tt.make_move(player = players[current_player], position = position)
        
        # Close the old plot
        plt.close()
        draw_board(tt.board)
        # tt.pretty_print_board()   
        winner = tt.check_for_winner()
        tie = tt.check_for_tie()
    if winner != None:
        print('{} wins'.format(players[current_player]))
    elif tie != None:
        print('The game is a draw')
    # Keep final plot open until pressing enter
    input('Press Enter to exit.')
