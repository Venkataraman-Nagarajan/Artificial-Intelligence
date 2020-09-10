import random 
import math

class Board_State:
    state = None
    cost = math.inf
    size = 0;
    
    def __init__(self,state):
        '''
        Used to initialize the state with No of queens 
        and the conflicts btw them as cost using cost function
        '''
        
        self.state = state
        self.size = len(state)
        self.cost = self.compute_conflict() # objective function
        
    def __str__(self): 
        '''
        Converting the state into a 2D- grid for readability
        '''
        string = "\n"
        
        for i in range(self.size):
            temp = "- " * (self.state[i]-1) + "Q " + "- " * (self.size - self.state[i] ) + "\n"
            string += '\t' + temp
        
        return string
        
    def compute_conflict(self): #
        '''
        Compute the No of conflicts in the board
        Conflict - > if Queen X attacks Queen Y , then it is a conflict
        So we try to find no of unique pairs showing conflicts btw queens 
        '''
        
        conflict = 0
        
        for i in range(self.size):
            for j in range(i+1,self.size):
                
                #check for same row
                if(self.state[i] == self.state[j]):
                    conflict+=1
                
                #check for left diagnol
                elif(self.state[i]+i == self.state[j]+j):
                    conflict+=1
                
                #check for right diagnol
                elif(self.state[i]-i == self.state[j]-j):
                    conflict+=1
        
        return conflict
    

# def next_best_state(board): 
#     '''
#     Finds the next best state (a state with minimum No of conflicts) 
#     to climb up the hill by comparing all other neighbours
#     Doesnot include sideway movements
#     Wont randomize the moves
#     This is enough for standard 14% success    
#     '''
#     best_state = board
    
#     for i in range(board.size):
#         start = board.state[i]
#         for j in range(1,board.size+1):
#             if(j != start):
#                 board.state[i] = j
                
#                 new_board = Board_State(list(board.state))
                
#                 if(new_board.cost < best_state.cost):
#                     best_state = new_board
                
#                 board.state[i] = start        
    
#     return best_state

def next_best_state(board):
    '''
    Finds the next best state (a state with minimum No of conflicts) 
    to climb up the hill by comparing all other neighbours. 
    Includes sideways moves, to move through the graph
    Randomizes the next state moves so that the chances of running 
    into an infinite loop is reduced
    '''
    best_state = board
    
    moves = []
    
    for i in range(board.size):
        start = board.state[i]
        for j in range(1,board.size+1):
            if(j != start):
                moves.append([i,j])
    
    random.shuffle(moves)
    
    for move in moves:
        i = move[0]
        j = move[1]
        
        start = board.state[i]
        board.state[i] = j

        new_board = Board_State(list(board.state))
        
        if(new_board.cost <= best_state.cost):
            best_state = new_board
        
        board.state[i] = start
    
    return best_state

def Hill_Climber(cur_board, max_iter = 10000):  
    '''
    Climbs up the Hill to find a local optimum value. 
    When a more optimum value is not found, We conclude that the 
    current state(cur_board) to be the local optimum value  
    '''
    
    next_board = next_best_state(cur_board)
    
    if(cur_board.cost != next_board.cost):
        return Hill_Climber(next_board)
    
    if(next_board.state == cur_board.state or max_iter==0):
        return next_board
    
    return Hill_Climber(next_board, max_iter-1)

if __name__ == "__main__":
    print("\t\tHill Climbing\n\t\t N - Queens\n")

    board_length = 8
    initial_board = Board_State([random.randint(1,board_length) for i in range(board_length)])
    #initial_board = Board_State([3,4,2,5,8,7,6,1])    
    #initial_board = Board_State([1,1,1,1,1,1,1,1])    
    Final_board = Hill_Climber(initial_board)
    
    print("Initial Board : ",initial_board)
    print("Conflict      : ",initial_board.cost)
    print("\n")
    
    print("Final Board   : ",Final_board)
    print("Conflict      : ",Final_board.cost)
    print()
    

'''
Output @05:30
                Hill Climbing
                 N - Queens

Initial Board :  
        - - Q - - - - - 
        - - - Q - - - - 
        - Q - - - - - - 
        - - - - Q - - - 
        - - - - - - - Q 
        - - - - - - Q - 
        - - - - - Q - - 
        Q - - - - - - - 

Conflict      :  7


Final Board   :  
        - - Q - - - - - 
        - - - - - Q - - 
        - Q - - - - - - 
        - - - - Q - - - 
        - - - - - - - Q 
        Q - - - - - - - 
        - - - - - - Q - 
        - - - Q - - - - 

Conflict      :  0

'''
'''
Output @05:30
                Hill Climbing
                 N - Queens

Initial Board :  
        - - - Q - - - - 
        - - Q - - - - - 
        - Q - - - - - - 
        - - - - Q - - - 
        - - - Q - - - - 
        - - Q - - - - - 
        - Q - - - - - - 
        - - Q - - - - - 

Conflict      :  17


Final Board   :  
        - - Q - - - - - 
        - - - - - Q - - 
        - Q - - - - - - 
        - - - - Q - - - 
        Q - - - - - - - 
        - - - Q - - - - 
        - - - - - - Q - 
        - - Q - - - - - 

Conflict      :  1

'''

'''
Output: 
		Hill Climbing
		 N - Queens

Initial Board :  
	Q - - - - - - - 
	Q - - - - - - - 
	Q - - - - - - - 
	Q - - - - - - - 
	Q - - - - - - - 
	Q - - - - - - - 
	Q - - - - - - - 
	Q - - - - - - - 

Conflict      :  28


Final Board   :  
	- - - - - Q - - 
	- - - Q - - - - 
	- Q - - - - - - 
	- - - - - - - Q 
	- - - - Q - - - 
	- - - - - - Q - 
	Q - - - - - - - 
	- - Q - - - - - 

Conflict      :  0

'''
