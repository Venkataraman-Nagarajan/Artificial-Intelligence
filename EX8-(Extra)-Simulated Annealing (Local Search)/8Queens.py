import random 
import math
import heapq

class Board_State:
    state = None
    value = math.inf
    size = 0;
    
    def __init__(self,state):
        '''
        Used to initialize the state with No of queens 
        and the conflicts btw them as fitness using fitness function
        '''
        
        self.state = state
        self.size = len(state)
        self.value = self.value_fn() # objective function
        
    def __str__(self): 
        '''
        Converting the state into a 2D- grid for readability
        '''
        string = "\n"
        
        for i in range(self.size):
            temp = "- " * (self.state[i]-1) + "Q " + "- " * (self.size - self.state[i] ) + "\n"
            string += '\t' + temp
        
        return string
    
    def __gt__(self,another_board):
        '''
        Comparator to compare two boards
        based on its fitness value
        '''
        
        return self.fitness <= another_board.fitness
    
    def value_fn(self): 
        '''
        Compute the No of non-conflicts in the board
        Conflict - > if Queen X attacks Queen Y , then it is a conflict
        So we try to find no of unique pairs not showing conflicts btw queens 
        '''
        
        conflict = self.size * (self.size-1) // 2
        
        for i in range(self.size):
            for j in range(i+1,self.size):
                
                #check for same row
                if(self.state[i] == self.state[j]):
                    conflict-=1
                
                #check for left diagnol
                elif(self.state[i]+i == self.state[j]+j):
                    conflict-=1
                
                #check for right diagnol
                elif(self.state[i]-i == self.state[j]-j):
                    conflict-=1
        
        return conflict

    def nextStates(self):
        '''
        Finds the set of next states reachable from the current state
        '''
        board = self
        
        moves = []
        
        for i in range(board.size):
            start = board.state[i]
            for j in range(1,board.size+1):
                if(j != start):
                    moves.append([i,j])
        
        random.shuffle(moves)
        nextBoard = []
        
        for move in moves:
            i = move[0]
            j = move[1]
            
            start = board.state[i]
            board.state[i] = j

            new_board = Board_State(list(board.state))
            
            nextBoard.append(new_board)
                
            board.state[i] = start
        
        return nextBoard
    
class SA_Solver:
    
    def schedule(self, t):
        '''
        The function maps time 't' to a Temperature and returns it
        '''
        
        return 1/(2*t)
    
    def randomSelect(self, List):
        '''
        randomly selects a item from a List of items
        '''
        
        sz = len(List)
        indx = random.randint(0, sz-1)
        
        return List[indx]
    
    def printProbablity(self):
        '''
        Returns 1 if we can print, else returns 0
        '''
        
        return random.random() < 0.01
    
    def Simulated_Annealing(self, current):
        '''
        Simulates the SA algorithm
        
        ALGORITHM :
            function SIMULATED-ANNEALING ( problem, schedule) returns a solution state
            inputs: problem, a problem
                    schedule, a mapping from time to “temperature”
            
            current ← MAKE-NODE (problem.INITIAL-STATE )
            for t = 1 to ∞ do
                T ← schedule(t )
                if T = 0 then return current
                next ← a randomly selected successor of current
                ΔE ← next.V ALUE – current.VALUE
                if ΔE > 0 then current ← next
                else current ← next only with probability e^(ΔE/T)
        
        '''
        
        time = 1
        prev = current.value
        while(True):
            T = self.schedule(time)
            if T <= 10**-4:
                return current
            
            Next = self.randomSelect(current.nextStates())
            
            del_E = Next.value - current.value
            
            if del_E > 0:
                current = Next
            elif random.random() < math.exp(del_E/T):
                current = Next
            
            if self.printProbablity() or time == 1 or prev != current.value:
                print("At time {0} -the current board has the value of {1} ".format(str(time).zfill(5), current.value))
                prev = current.value
            
            time+=1
            
        return current
            
    
if __name__ == "__main__":
    print("\t\tSimulated Annealing Algorithm\n\t\t\t N - Queens\n")
    
    board_length = 8
    initial_board = Board_State([random.randint(1,board_length) for i in range(board_length)])
    #initial_board = Board_State([1,2,3,4,5,6,7,8])
    SA_agent = SA_Solver()
    
    print("Initial Board : ",initial_board)
    print("Value         : ",initial_board.value)
    print("\n")
    
    Final_board = SA_agent.Simulated_Annealing(initial_board)
    
    print("\nFinal Board   : ",Final_board)
    print("Value         : ",Final_board.value)
    print()
    
'''
OUTPUT :
               Simulated Annealing Algorithm
                         N - Queens

Initial Board :  
        - Q - - - - - - 
        - - - - - - - Q 
        Q - - - - - - - 
        - - Q - - - - - 
        - - - - - Q - - 
        Q - - - - - - - 
        - - - - - - Q - 
        - - Q - - - - - 

Value         :  22


At time 00001 -the current board has the value of 22 
At time 01132 -the current board has the value of 28 
At time 01324 -the current board has the value of 28 
At time 01610 -the current board has the value of 28 
At time 01705 -the current board has the value of 28 
At time 02103 -the current board has the value of 28 
At time 02296 -the current board has the value of 28 
At time 03096 -the current board has the value of 28 
At time 04280 -the current board has the value of 28 

Final Board   :  
        - - - - - Q - - 
        - - - Q - - - - 
        - - - - - - Q - 
        Q - - - - - - - 
        - - - - - - - Q 
        - Q - - - - - - 
        - - - - Q - - - 
        - - Q - - - - - 

Value         :  28

'''

'''
OUTPUT :
                Simulated Annealing Algorithm
                         N - Queens

Initial Board :  
        Q - - - - - - - 
        - Q - - - - - - 
        - - Q - - - - - 
        - - - Q - - - - 
        - - - - Q - - - 
        - - - - - Q - - 
        - - - - - - Q - 
        - - - - - - - Q 

Value         :  0


At time 00001 -the current board has the value of 5 
At time 00002 -the current board has the value of 11 
At time 00003 -the current board has the value of 15 
At time 00008 -the current board has the value of 16 
At time 00010 -the current board has the value of 18 
At time 00011 -the current board has the value of 20 
At time 00017 -the current board has the value of 21 
At time 00019 -the current board has the value of 22 
At time 00025 -the current board has the value of 25 
At time 00035 -the current board has the value of 25 
At time 00066 -the current board has the value of 26 
At time 00245 -the current board has the value of 27 
At time 00307 -the current board has the value of 27 
At time 00394 -the current board has the value of 27 
At time 00556 -the current board has the value of 27 
At time 00636 -the current board has the value of 27 
At time 00664 -the current board has the value of 27 
At time 00668 -the current board has the value of 27 
At time 00679 -the current board has the value of 27 
At time 00748 -the current board has the value of 27 
At time 00946 -the current board has the value of 27 
At time 01054 -the current board has the value of 28 
At time 01075 -the current board has the value of 28 
At time 01215 -the current board has the value of 28 
At time 01379 -the current board has the value of 28 
At time 01748 -the current board has the value of 28 
At time 01761 -the current board has the value of 28 
At time 01845 -the current board has the value of 28 
At time 02002 -the current board has the value of 28 
At time 02124 -the current board has the value of 28 
At time 02155 -the current board has the value of 28 
At time 02162 -the current board has the value of 28 
At time 02204 -the current board has the value of 28 
At time 02236 -the current board has the value of 28 
At time 02264 -the current board has the value of 28 
At time 02417 -the current board has the value of 28 
At time 02431 -the current board has the value of 28 
At time 02585 -the current board has the value of 28 
At time 02620 -the current board has the value of 28 
At time 02701 -the current board has the value of 28 
At time 02757 -the current board has the value of 28 
At time 02779 -the current board has the value of 28 
At time 02827 -the current board has the value of 28 
At time 02874 -the current board has the value of 28 
At time 03190 -the current board has the value of 28 
At time 03364 -the current board has the value of 28 
At time 03576 -the current board has the value of 28 
At time 03676 -the current board has the value of 28 
At time 03681 -the current board has the value of 28 
At time 03707 -the current board has the value of 28 
At time 03825 -the current board has the value of 28 
At time 03829 -the current board has the value of 28 
At time 04020 -the current board has the value of 28 
At time 04094 -the current board has the value of 28 
At time 04129 -the current board has the value of 28 
At time 04187 -the current board has the value of 28 
At time 04426 -the current board has the value of 28 
At time 04593 -the current board has the value of 28 
At time 04595 -the current board has the value of 28 
At time 04856 -the current board has the value of 28 
At time 04967 -the current board has the value of 28 

Final Board   :  
        - - - - - - Q - 
        - - - Q - - - - 
        - Q - - - - - - 
        - - - - Q - - - 
        - - - - - - - Q 
        Q - - - - - - - 
        - - Q - - - - - 
        - - - - - Q - - 

Value         :  28
'''