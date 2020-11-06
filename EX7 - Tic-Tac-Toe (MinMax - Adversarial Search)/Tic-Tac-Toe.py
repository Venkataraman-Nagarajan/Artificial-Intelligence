import math
from copy import deepcopy

class Board:
    
    def __init__(self,board = [['.','.','.'],['.','.','.'],['.','.','.']]):
        '''
        This class takes in the board that is the current game play
        board, and has functions related to queries regarding the 
        board state
        '''
        
        self.board_state = board
    
    def __str__(self):
        '''
        Converts the 2D - board list into human readable form
        '''
        
        string  = ""
        
        for i, row in enumerate(self.board_state):
            string += '\t'
            for j,val in enumerate(row):
                
                if val != 'X' and val != 'O':
                    string += ' - '
                else:
                    string += ' ' +  val + ' '
                
                if j != len(row)-1:
                    string += '|'
            
            if i != len(self.board_state)-1:
                string += '\n\t--- --- ---\n'
            
        return string
                
    
    def getValue(self):
        '''
        The function uses the current instance of the board state
        and computes the reward of this board at that instant.
        
        reward(s):
               (+)10 - If X wins (Trying to maximize the reward)
               (-)10 - If O wins (Trying to minimize the reward)
               (±) 0 - If its a draw state
        
        Winning states in Tic-Tac-Toe are :
            [X X X]  [- - -]  [- - -]   
            [- - -]  [X X X]  [- - -]  
            [- - -]  [- - -]  [X X X]
            
            [X - -]  [- X -]  [- - X]   
            [X - -]  [- X -]  [- - X]  
            [X - -]  [- X -]  [- - X]  
            
            [X - -]  [- - X]     
            [- X -]  [- X -]    
            [- - X]  [X - -]
              
        '''
        
        board = self.board_state
        winning  = [
                    [board[0][0],board[0][1],board[0][2]],
                    [board[1][0],board[1][1],board[1][2]],
                    [board[2][0],board[2][1],board[2][2]],
                    
                    [board[0][0],board[1][0],board[2][0]],
                    [board[0][1],board[1][1],board[2][1]],
                    [board[0][2],board[1][2],board[2][2]],

                    [board[0][0],board[1][1],board[2][2]],
                    [board[0][2],board[1][1],board[2][0]],                    
                    ]

        if ['X', 'X', 'X'] in winning:
            return 10
        
        elif ['O', 'O', 'O'] in winning:
            return -10
        
        return 0
    
    def isLeft(self):
        '''
        Finds whether there is a location in the board that is vacant.
        If present returns True, else returns False 
        '''
        
        board  = self.board_state
        for row in board:
            for val in row:
                if val == '.' or val == ' ':
                    return True
        
        return False
    
    def nextMoves(self):
        '''
        Finds all the vacant locations in the board to fill
        for next move
        '''
        
        board  = self.board_state
        next_moves = []
        for i,row in enumerate(board):
            for j,val in enumerate(row):
                if val == '.' or val == ' ':
                    next_moves.append((i,j))
        
        return next_moves
    
    def isTerminal(self):
        '''
        The Function checks whether the board is in an end-state of the 
        game
        
        End-State can be defined as a state where a clear winner is found
        or a state from which no next moves exists
        '''
        
        if self.getValue():
            return True
        if not self.isLeft():
            return True
        
        return False

'''
Constants to indicate who is playing on a particular side
a symbol is specified as COMP/USER

COMP - indicates that the symbol is played by the Computer-AI.
USER - indicates that the symbol is played by the user-Input.
'''
COMP = 1
USER = 0

class Game:
    
    def __init__(self):
        '''
        This class is used to perform game play of Tic-Tac-Toe 
        ''' 
        
        self.map = {1 : 'X', 0 : 'O'}
        
    
    def user_move(self, turn, board):
        '''
        This function ask the user his move to play in the board
        
        This is the format of the board:
        
         1 | 2 | 3 
        --- --- ---
         4 | 5 | 6 
        --- --- ---
         7 | 8 | 9 
         
        The user will be asked to place his/her symbol in the board 
        using 1-9 position.
        '''
        
        if board.isTerminal():
            return board
        
        print('Available Moves are :  ',end = "")
        
        moves = board.nextMoves()
        
        for indx,move in enumerate(moves):
            print(move[0]*3 + move[1] + 1, end = "")
            if indx != len(moves)-1:
                print(', ',end="")
        
        chosenMove = (-1,-1)
        
        while chosenMove not in moves:
            print('\nEnter your Move to place ',self.map[turn] ,' in the board')
            print('---> ',end = " ")
            choice = int(input())
        
            print()
            
            chosenMove = ((choice-1)//3,(choice-1)%3)

            if chosenMove not in moves:
                print('Please enter from available moves\n')
        
        newBoard_state = deepcopy(board.board_state)
        newBoard_state[chosenMove[0]][chosenMove[1]] = self.map[turn]
                
        newBoard = Board(newBoard_state)
            
        return newBoard

    '''
    For alpha_beta_search - max_value - min_value
    
    function ALPHA-BETA-SEARCH (state) returns an action
        v ← MAX-VALUE(state, −∞, +∞) / MIN-VALUE(state, −∞, +∞)
        return the action in ACTIONS(state) with value v

    function MAX-VALUE (state, α, β) returns a utility value
        if TERMINAL-TEST (state) then return UTILITY (state)
        v ← −∞
        for each a in ACTIONS (state) do
            v ← MAX (v , MIN-VALUE (RESULT (s,a), α, β))
            if v ≥ β then return v
            α ← MAX (α, v )
        return v
        
    function MIN -VALUE (state, α, β) returns a utility value
        if TERMINAL -TEST (state) then return UTILITY (state)
        v ← +∞
        for each a in A CTIONS (state) do
            v ← MIN (v , MAX-VALUE (RESULT (s,a) , α, β))
            if v ≤ α then return v
            β ← MIN (β, v )
        return v
    '''
    
    
    def max_value(self, board, alpha = -math.inf, beta = +math.inf):
        
        if board.isTerminal():
            return board.getValue(), board
        
        bestVal = -math.inf
        bestBoard = None
         
        for move in board.nextMoves():
            newBoard_state = deepcopy(board.board_state)
            newBoard_state[move[0]][move[1]] = 'X'
                
            newBoard = Board(newBoard_state)
            
            cost, res_board = self.min_value(newBoard, alpha, beta)
            
            if bestVal < cost:
                bestVal = cost
                bestBoard = newBoard
                
            alpha = max(alpha, bestVal)
                
            if beta <= alpha:
                break
        
        return bestVal, bestBoard
        
    def min_value(self, board, alpha = -math.inf, beta = +math.inf):
        
        if board.isTerminal():
            return board.getValue(), board
        
        bestVal = +math.inf
        bestBoard = None
         
        for move in board.nextMoves():
            newBoard_state = deepcopy(board.board_state)
            newBoard_state[move[0]][move[1]] = 'O'
                
            newBoard = Board(newBoard_state)
            
            cost, res_board = self.max_value(newBoard, alpha, beta)
            
            if bestVal > cost:
                bestVal = cost
                bestBoard = newBoard
                
            beta = min(beta, bestVal)
                
            if beta <= alpha:
                break
        
        return bestVal, bestBoard
        

    def alpha_beta_search(self,turn ,board):
        '''
        This function does alpha-beta pruning and calls functions
        based on whose turn it is
        
        If the requirement is to maximize the answer , then max_value is called
        Else if the requirement is to minimize the answer , then min_value is called 
        '''
        
        if turn == 1:
            result_board = self.max_value(deepcopy(board))
        else:
            result_board = self.min_value(deepcopy(board))
            
        return result_board
    
    def game_play(self, X_player = COMP, O_player = COMP):
        '''
        This function is used to simulate the whole game and
        print every instance of the game.
        '''
        
        board  = Board([['.','.','.'],['.','.','.'],['.','.','.']])
        turn = 1
        
        print('Current Board position : ')
        print(board)
        print()
        
        player = {1 : X_player, 0 : O_player}
        
        while not board.isTerminal():
            
            if player[turn] == COMP:
                cost, board = self.alpha_beta_search(turn, board)    
            else:
                print(self.map[turn],'\'s turn - ')
                board = self.user_move(turn, board)
            
            print(self.map[turn],' Moves : ')    
            print(board)
            print()
        
            turn = 1 - turn
        
        prize = board.getValue()
        
        if prize == 0:
            print('\n\tITS A DRAW\n')
        elif prize == 10:
            print('\n\tX Wins\n')
        elif prize == -10:
            print('\n\tO wins\n')

if __name__ == '__main__':
    '''
    The Function explores all four options of playing 
    Tic - Tac - Toe
    
    (.) opt 1 - COMPUTER VS COMPUTER
    (.) opt 2 - USER     VS COMPUTER
    (.) opt 3 - COMPUTER VS USER
    (.) opt 4 - USER     VS USER
    
    '''
    
    print('\t\t  Adversarial Search \n')
    print('\t\t❌ Tic - Tac - Toe 🇴\n\n')
    
    solver = Game()
    
    # uncomment/comment next line to explore/stop opt 1.
    # solver.game_play()
    
    # uncomment/comment next line to explore/stop opt 2.
    # solver.game_play(X_player=USER)

    # uncomment/comment next line to explore/stop opt 3.
    # solver.game_play(O_player=USER)
    
    # uncomment/comment next line to explore/stop opt 4.
    solver.game_play(X_player=USER, O_player=USER)
    

'''
                  Adversarial Search 

                ❌ Tic - Tac - Toe 🇴


Current Board position : 
         - | - | - 
        --- --- ---
         - | - | - 
        --- --- ---
         - | - | - 

X 's turn - 
Available Moves are :  1, 2, 3, 4, 5, 6, 7, 8, 9
Enter your Move to place  X  in the board
--->  5

X  Moves : 
         - | - | - 
        --- --- ---
         - | X | - 
        --- --- ---
         - | - | - 

O  Moves : 
         O | - | - 
        --- --- ---
         - | X | - 
        --- --- ---
         - | - | - 

X 's turn - 
Available Moves are :  2, 3, 4, 6, 7, 8, 9
Enter your Move to place  X  in the board
--->  3

X  Moves : 
         O | - | X 
        --- --- ---
         - | X | - 
        --- --- ---
         - | - | - 

O  Moves : 
         O | - | X 
        --- --- ---
         - | X | - 
        --- --- ---
         O | - | - 

X 's turn - 
Available Moves are :  2, 4, 6, 8, 9
Enter your Move to place  X  in the board
--->  2

X  Moves : 
         O | X | X 
        --- --- ---
         - | X | - 
        --- --- ---
         O | - | - 

O  Moves : 
         O | X | X 
        --- --- ---
         O | X | - 
        --- --- ---
         O | - | - 


O wins

'''

'''
OUTPUT:
                  Adversarial Search 

                ❌ Tic - Tac - Toe 🇴


Current Board position : 
         - | - | - 
        --- --- ---
         - | - | - 
        --- --- ---
         - | - | - 

X  Moves : 
         X | - | - 
        --- --- ---
         - | - | - 
        --- --- ---
         - | - | - 

O  Moves : 
         X | - | - 
        --- --- ---
         - | O | - 
        --- --- ---
         - | - | - 

X  Moves : 
         X | X | - 
        --- --- ---
         - | O | - 
        --- --- ---
         - | - | - 

O  Moves : 
         X | X | O 
        --- --- ---
         - | O | - 
        --- --- ---
         - | - | - 

X  Moves : 
         X | X | O 
        --- --- ---
         - | O | - 
        --- --- ---
         X | - | - 

O  Moves : 
         X | X | O 
        --- --- ---
         O | O | - 
        --- --- ---
         X | - | - 

X  Moves : 
         X | X | O 
        --- --- ---
         O | O | X 
        --- --- ---
         X | - | - 

O  Moves : 
         X | X | O 
        --- --- ---
         O | O | X 
        --- --- ---
         X | O | - 

X  Moves : 
         X | X | O 
        --- --- ---
         O | O | X 
        --- --- ---
         X | O | X 


ITS A DRAW

'''
