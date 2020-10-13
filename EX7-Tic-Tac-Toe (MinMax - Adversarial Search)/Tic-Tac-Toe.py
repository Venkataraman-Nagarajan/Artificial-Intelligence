import math
from copy import deepcopy

class Board:
    
    def __init__(self,board = [['.','.','.'],['.','.','.'],['.','.','.']]):
        self.board_state = board
    
    def __str__(self):
        
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
        board  = self.board_state
        for row in board:
            for val in row:
                if val == '.' or val == ' ':
                    return True
        
        return False
    
    def nextMoves(self):
        board  = self.board_state
        next_moves = []
        for i,row in enumerate(board):
            for j,val in enumerate(row):
                if val == '.' or val == ' ':
                    next_moves.append((i,j))
        
        return next_moves
    
    def isTerminal(self):
        if self.getValue():
            return True
        if not self.isLeft():
            return True
        
        return False

COMP = 1
USER = 0

class Game:
    
    def __init__(self):
         
        self.map = {1 : 'X', 0 : 'O'}
        
    
    def user_move(self, turn, board):
        '''
         1 | 2 | 3 
        --- --- ---
         4 | 5 | 6 
        --- --- ---
         7 | 8 | 9 
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
            print()
            
            choice = int(input())
        
            chosenMove = ((choice-1)//3,(choice-1)%3)

            if chosenMove not in moves:
                print('Please enter from available moves\n')
        
        newBoard_state = deepcopy(board.board_state)
        newBoard_state[chosenMove[0]][chosenMove[1]] = self.map[turn]
                
        newBoard = Board(newBoard_state)
            
        return newBoard

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
        
        if turn == 1:
            result_board = self.max_value(deepcopy(board))
        else:
            result_board = self.min_value(deepcopy(board))
            
        return result_board
    
    def game_play(self, X_player = COMP, O_player = COMP):
        
        board  = Board([['.','.','.'],['.','.','.'],['.','.','.']])
        turn = 1
        
        print('Current Board position : ')
        print(board)
        print()
        
        player = {1 : X_player, 0 : O_player}
        
        while not board.isTerminal():
            
            
            if player[turn]:
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
    print('\t\t  Adversarial Search \n')
    print('\t\t❌ Tic - Tac - Toe 🇴\n\n')
    solver = Game()
    solver.game_play(X_player=USER)

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
