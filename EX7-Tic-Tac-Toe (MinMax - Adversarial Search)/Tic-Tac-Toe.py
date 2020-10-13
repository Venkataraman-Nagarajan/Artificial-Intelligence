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
    
    def game_play(self, player1 = COMP, player2 = COMP):
        
        board  = Board([['.','.','.'],['.','.','.'],['.','.','.']])
        turn = 1
        
        print('Current Board position : ')
        print(board)
        print()
        
        map = {1 : 'O', 0 : 'X'}
        
        #cost, board = self.alpha_beta_search(turn, board)    
            
        while not board.isTerminal():
            
            cost, board = self.alpha_beta_search(turn, board)    
            
            print(map[turn],' Moves : ')
            print(board)
            print()
        
            turn = 1 - turn
        
        prize = board.getValue()
        
        if prize == 0:
            print('\nITS A DRAW\n')
        elif prize == 10:
            print('\nX Wins\n')
        elif prize == -10:
            print('\nO wins\n')

if __name__ == '__main__':
    solver = Game()
    solver.game_play()

'''
OUTPUT:

Current Board position : 
         - | - | - 
        --- --- ---
         - | - | - 
        --- --- ---
         - | - | - 

O  Moves : 
         X | - | - 
        --- --- ---
         - | - | - 
        --- --- ---
         - | - | - 

X  Moves : 
         X | - | - 
        --- --- ---
         - | O | - 
        --- --- ---
         - | - | - 

O  Moves : 
         X | X | - 
        --- --- ---
         - | O | - 
        --- --- ---
         - | - | - 

X  Moves : 
         X | X | O 
        --- --- ---
         - | O | - 
        --- --- ---
         - | - | - 

O  Moves : 
         X | X | O 
        --- --- ---
         - | O | - 
        --- --- ---
         X | - | - 

X  Moves : 
         X | X | O 
        --- --- ---
         O | O | - 
        --- --- ---
         X | - | - 

O  Moves : 
         X | X | O 
        --- --- ---
         O | O | X 
        --- --- ---
         X | - | - 

X  Moves : 
         X | X | O 
        --- --- ---
         O | O | X 
        --- --- ---
         X | O | - 

O  Moves : 
         X | X | O 
        --- --- ---
         O | O | X 
        --- --- ---
         X | O | X 


ITS A DRAW

'''
