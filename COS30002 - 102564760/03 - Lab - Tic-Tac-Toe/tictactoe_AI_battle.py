'''Tic-Tac-Toe, Object Oriented Version

Created for COS30002 AI for Games, Lab,
by Clinton Woodward <cwoodward@swin.edu.au>

For class use only. Do not publically share or post this code without
permission.

Notes/Tips:
* Exactly the same behaviour as the function based version (tictactoe_cli.py).
* Very simple single class conversion of functions and global variables
* Game loop still controlled by the three input/update/render methods
* Internal class helper functions are marked by a leading "_"

General Python Notes:
* All class methods have "self" as their first parameter
* All class variables/methods need to be accessed by a leading "self."

'''

from random import choice, randrange


class TicTacToe(object):
    # class variables - belong to the *class* - NOT object instance.
    WIN_SET = (
        (0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
        (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)
    )
    

    HR = '-' * 40

    def __init__(self):
        # class instance variables for game data (were global variables)
        self.board = [' '] * 9
        self.players = {'x': 'Human', 'o': 'Super AI' }
        self.winner = None
        self.move = None
        # by default the human player starts. This could be random or a choice.
        rn = randrange(2)
        p = 'x'
        if rn == 0:
            p = 'x'
        if rn == 1:
            p = 'o'
        self.current_player = p
        # Welcome ...
        print('Welcome to the amazing+awesome tic-tac-toe!')
        # Show help (number) details
        self.show_human_help()
        # show the initial board and the current player's move
        self.render_board()

    def _check_move(self):
        '''This function will return True if ``move`` is valid (in the board range
        and free cell), or print an error message and return False if not valid.
        ``move`` is an int board position [0..8].
        '''
        try:
            self.move = int(self.move)
            if self.board[self.move] == ' ':
                return True
            else:
                print('>> Sorry - that position is already taken!')
                return False
        except:  # bare except bad practice but works
            print('>> %s is not a valid position! Must be int between 0 and 8.' % self.move)
            return False


    def _check_for_result(self):
        '''Checks the current board to see if there is a winner, tie or not.
        Returns a 'x' or 'o' to indicate a winner, 'tie' for a stale-mate game, or
        simply False if the game is still going.
        '''
        board = self.board
        for row in self.WIN_SET:
            if board[row[0]] == board[row[1]] == board[row[2]] != ' ':
                return board[row[0]] # return an 'x' or 'o' to indicate winner

        if ' ' not in board:
            return 'tie'

        return None

    #===========================================================================
    # agent (human or AI) functions

    def get_definately_not_an_ai_move(self):
        '''Get a "human" players raw input '''
        if self.go_last_space() <= 8:
            return self.go_last_space()
        
        #go to a random space next to the last move
        if self.move != None:
            return choice(self.adjacent.get(self.move, (randrange(9))))
        
        return randrange(9)
        

    def get_ai_move(self):
        '''Get the AI's next move '''

        if self.go_last_space() <= 8:
            return self.go_last_space()
        
        if self.board[4] == ' ':
            return 4
        
        return randrange(9) 

    def go_last_space(self):
        #search the board for potential winning spaces and return the last one
        board = self.board
        for row in self.WIN_SET:
            if (board[row[0]] == board[row[1]] != ' ') and (board[row[2]] == ' '):
                return row[2]
            if (board[row[1]] == board[row[2]] != ' ') and (board[row[0]] == ' '):
                return row[0]
            if (board[row[0]] == board[row[2]] != ' ') and (board[row[1]] == ' '):
                return row[1]
        #return an invalid move otherwise to tell the ai to make a different move
        return 9
    
    adjacent = {
        0: (1, 3),
        1: (0, 4, 2),
        2: (1, 5),
        3: (0, 4, 6),
        4: (1, 3, 5, 7),
        5: (2, 4, 8),
        6: (3, 7),
        7: (6, 4, 8),
        8: (7, 5)
    }


    #===========================================================================
    # Standard trinity of game loop methods (functions)

    def process_input(self):
        '''Get the current players next move.'''
        if self.current_player == 'x':
            self.move = self.get_definately_not_an_ai_move()
        else:
            self.move = self.get_ai_move()

    def update_model(self):
        '''If the current players input is a valid move, update the board and check
        the game model for a winning player. If the game is still going, change the
        current player and continue. If the input was not valid, let the player
        have another go.
        '''
        if self._check_move():
            # do the new move (which is stored in the instance 'move' variable)
            self.board[self.move] = self.current_player
            # check board for winner (now that it's been updated)
            self.winner = self._check_for_result()
            # change the current player (regardless of the outcome)
            if self.current_player == 'x':
                self.current_player = 'o'
            else:
                self.current_player = 'x'
        else:
            print('Try again')

    def render_board(self):
        '''Display the current game board to screen.'''
        board = self.board
        print('    %s | %s | %s' % tuple(board[:3]))
        print('   -----------')
        print('    %s | %s | %s' % tuple(board[3:6]))
        print('   -----------')
        print('    %s | %s | %s' % tuple(board[6:]))

        # pretty print the current player name
        if self.winner is None:
            print('The current player is: %s' % self.players[self.current_player])

    def show_human_help(self):
        '''Show the player help/instructions. '''
        tmp = '''\
    To make a move enter a number between 0 - 8 and press enter.
    The number corresponds to a board position as illustrated:

        0 | 1 | 2
        ---------
        3 | 4 | 5
        ---------
        6 | 7 | 8
        '''
        print(tmp)
        print(self.HR)

    def show_gameresult(self):
        '''Show the game result winner/tie details'''
        print(self.HR)
        if self.winner == 'tie':
            print('TIE!')
        else:
            print('%s is the WINNER!!!' % self.players[self.winner])
        print(self.HR)
        print('Game over. Goodbye')


if __name__ == '__main__':
    # create instance (~ "new") object of type TicTacToe class
    game = TicTacToe()

    # Standard game loop structure
    while game.winner is None:
        game.process_input()
        game.update_model()
        game.render_board()

    
    game.show_gameresult()