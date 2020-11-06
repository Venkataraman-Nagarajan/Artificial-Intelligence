from collections import deque
import heapq

class Puzzle_State:
    
    state = None
    parent = None
    operation = None
    
    zero = (-1,-1)
    
    cost = 0
    depth = 0
    isBackward = False
    
    goal_state = ((0,1,2),(3,4,5),(6,7,8))
    
    def __init__(self,state, parent = None, operation = None, depth = 0, isBackward = False):
        
        self.state = state
        self.parent = parent        
        self.operation = operation
        
        self.zero = self.pos_zero()
        self.depth = depth
        self.isBackward = isBackward
        
        self.cost = self.heuristic_val()
        if isBackward == True:
            self.cost += self.depth 
        
    def __str__(self):
        return '\t' + str(list(self.state[0])) + '\n' \
            +  '\t' + str(list(self.state[1])) + '\n' \
            +  '\t' + str(list(self.state[2])) + '\n' 
    
    def __lt__(self,board):
        if self.cost == board.cost:
            return self.depth < board.depth
        return self.cost < board.cost
    
    def is_goal_state(self):
        return self.state == self.goal_state
    
    def pos_zero(self):
        for i in range(len(self.state)):
            for j in range(len(self.state[0])):
                if(self.state[i][j] == 0):
                    return (i,j)
    
    def swap(self, i, j):
        new_state = list(self.state)
        new_state = [list(x) for x in new_state]
        
        #print(new_state, i , j)
        new_state[i[0]][i[1]], new_state[j[0]][j[1]] = new_state[j[0]][j[1]], new_state[i[0]][i[1]]
        
        new_state = tuple([tuple(x) for x  in new_state])
        return new_state
    
    def move_down(self):
        if(self.zero[0] != 0):
            return Puzzle_State(self.swap(self.zero, (self.zero[0]-1, self.zero[1])), self, "DOWN \\/", self.depth+1, self.isBackward)
        return None
    
    def move_up(self):
        if(self.zero[0] != len(self.state)-1):
            return Puzzle_State(self.swap(self.zero, (self.zero[0]+1, self.zero[1])), self, "UP /\\  ", self.depth+1, self.isBackward)
        return None
    
    def move_right(self):
        if(self.zero[1] != 0):
            return Puzzle_State(self.swap(self.zero, (self.zero[0], self.zero[1]-1)), self, "RIGHT > ", self.depth+1, self.isBackward)
        return None
    
    def move_left(self):
        if(self.zero[1] != len(self.state[0]) - 1 ):
            return Puzzle_State(self.swap(self.zero, (self.zero[0], self.zero[1]+1)), self, "LEFT <  ", self.depth+1, self.isBackward)
        return None

    def next_states(self):
        next_states = []
        next_states.append(self.move_up())
        next_states.append(self.move_down())
        next_states.append(self.move_left())
        next_states.append(self.move_right())
        
        next_states = list(filter(None, next_states))
        return next_states
    
    def heuristic_val(self):
        
        heuristic = 0
        
        for val in range(1,9):
            x = [-1,-1]
            y = [-1,-1]
            
            for i in range(len(self.state)):
                for j in range(len(self.state[0])):
                    if(self.state[i][j]==val):
                        x = [i,j]
                    if(self.goal_state[i][j]==val):
                        y = [i,j]
            
            heuristic += abs(x[0]-y[0]) + abs(x[1]-y[1])
        return heuristic
            
                        
class Puzzle_Solver:
    
    solution = None
    current_depth = 0
    No_of_states = 0
    
    def BFS(self, init_state):  #trverses the whole graph (state space here ) only once
        
        frontier = deque()
        visited = set()
        
        frontier.append(init_state)
        visited.add(init_state.state)
        
        while(frontier):
            board = frontier.popleft()
            
            if board.is_goal_state():
                self.solution = board
                self.No_of_states = len(visited)
                return self.solution
            
            for next_state in board.next_states():
                if(next_state.state not in visited):
                    visited.add(next_state.state)
                    frontier.append(next_state)  
                    self.current_depth = max(self.current_depth, next_state.depth)          

        self.No_of_states = len(visited)
        return None
    
    def GBFS(self, init_state):
        
        frontier = []
        explored = set()
        visited = set()
        
        heapq.heappush(frontier, init_state)
        visited.add(init_state.state)
        
        while(frontier):
            
            board = heapq.heappop(frontier)
            
            if(board.state in explored):
                continue
            
            explored.add(board.state)
            
            if board.is_goal_state():
                self.solution = board
                break
            
            for next_state in board.next_states():
                if(next_state.state not in visited):
                    visited.add(next_state.state)
                    heapq.heappush(frontier, next_state)
                    self.current_depth = max(self.current_depth, next_state.depth)
                elif(next_state.state not in explored):
                    heapq.heappush(frontier, next_state)
                    self.current_depth = max(self.current_depth, next_state.depth)
            
            
        self.No_of_states = len(visited)
        return self.solution
    
    def A_STAR(self, init_state):
        
        frontier = []
        explored = set()
        visited = set()
        
        heapq.heappush(frontier, init_state)
        visited.add(init_state.state)
        
        while(frontier):
            
            board = heapq.heappop(frontier)
            
            if(board.state in explored):
                continue
            
            explored.add(board.state)
            
            if board.is_goal_state():
                self.solution = board
                break
            
            for next_state in board.next_states():
                if(next_state.state not in visited):
                    visited.add(next_state.state)
                    heapq.heappush(frontier, next_state)
                    self.current_depth = max(self.current_depth, next_state.depth)
                elif(next_state.state not in explored):
                    heapq.heappush(frontier, next_state)
                    self.current_depth = max(self.current_depth, next_state.depth)
            
            
        self.No_of_states = len(visited)
        return self.solution
                
    def trace_path(self): 
        this_state = self.solution
        path = [this_state]
        
        while(this_state.parent != None):
            path.append(this_state.parent)
            this_state = this_state.parent
        
        return path[::-1]
        
    def printPath(self):
        print("No. of states found        : ", self.No_of_states)
        print("Depth Reached              : ", self.current_depth)
        
        if(self.solution == None):
            print("Goal State Not Found !!\n")
            return
        
        PATH = self.trace_path()
        print("No. of Moves to reach goal : ", len(PATH)-1)
        print()
        
        print("Path to reach Goal state:- ")
        for State in PATH:
            print("  Move : ",State.operation)
            print(State , '\n')
        print('\t\t => Goal State')
        print()


if __name__ == "__main__":
    print("\t\t -> 8-PUZZLE PROBLEM <-")
    
    print("\n------------------------------------------------------------\n")
    
    print("\t Uninformed Search - Breath First Search \n")
    solver = Puzzle_Solver()
    initial_board = ((7,2,4), (5,0,6) , (8,3,1));
    init_state = Puzzle_State(initial_board);
    solution = solver.BFS(init_state)
    solver.printPath()
        
    print("\n------------------------------------------------------------\n")
    
    print("\n\t Informed Search - Greedy Best First Search \n")
    solver = Puzzle_Solver()
    initial_board = ((7,2,4), (5,0,6) , (8,3,1));
    init_state = Puzzle_State(initial_board);
    solution = solver.GBFS(init_state)
    solver.printPath()
        
    print("\n------------------------------------------------------------\n")
    
    print("\n\t Informed Search - A* Search \n")
    solver = Puzzle_Solver()
    initial_board = ((7,2,4), (5,0,6) , (8,3,1));
    init_state = Puzzle_State(initial_board,None,None,0,True);
    solution = solver.A_STAR(init_state)
    solver.printPath()
        
    print("\n------------------------------------------------------------\n")
    

'''
OUTPUT: 
                 -> 8-PUZZLE PROBLEM <-

------------------------------------------------------------

         Uninformed Search - Breath First Search 

No. of states found        :  178351
Depth Reached              :  27
No. of Moves to reach goal :  26

Path to reach Goal state:- 
  Move :  None
        [7, 2, 4]
        [5, 0, 6]
        [8, 3, 1]
 

  Move :  RIGHT > 
        [7, 2, 4]
        [0, 5, 6]
        [8, 3, 1]
 

  Move :  DOWN \/
        [0, 2, 4]
        [7, 5, 6]
        [8, 3, 1]
 

  Move :  LEFT <  
        [2, 0, 4]
        [7, 5, 6]
        [8, 3, 1]
 

  Move :  UP /\  
        [2, 5, 4]
        [7, 0, 6]
        [8, 3, 1]
 

  Move :  UP /\  
        [2, 5, 4]
        [7, 3, 6]
        [8, 0, 1]
 

  Move :  RIGHT > 
        [2, 5, 4]
        [7, 3, 6]
        [0, 8, 1]
 

  Move :  DOWN \/
        [2, 5, 4]
        [0, 3, 6]
        [7, 8, 1]
 

  Move :  LEFT <  
        [2, 5, 4]
        [3, 0, 6]
        [7, 8, 1]
 

  Move :  LEFT <  
        [2, 5, 4]
        [3, 6, 0]
        [7, 8, 1]
 

  Move :  DOWN \/
        [2, 5, 0]
        [3, 6, 4]
        [7, 8, 1]
 

  Move :  RIGHT > 
        [2, 0, 5]
        [3, 6, 4]
        [7, 8, 1]
 

  Move :  RIGHT > 
        [0, 2, 5]
        [3, 6, 4]
        [7, 8, 1]
 

  Move :  UP /\  
        [3, 2, 5]
        [0, 6, 4]
        [7, 8, 1]
 

  Move :  LEFT <  
        [3, 2, 5]
        [6, 0, 4]
        [7, 8, 1]
 

  Move :  LEFT <  
        [3, 2, 5]
        [6, 4, 0]
        [7, 8, 1]
 

  Move :  UP /\  
        [3, 2, 5]
        [6, 4, 1]
        [7, 8, 0]
 

  Move :  RIGHT > 
        [3, 2, 5]
        [6, 4, 1]
        [7, 0, 8]
 

  Move :  DOWN \/
        [3, 2, 5]
        [6, 0, 1]
        [7, 4, 8]
 

  Move :  LEFT <  
        [3, 2, 5]
        [6, 1, 0]
        [7, 4, 8]
 

  Move :  DOWN \/
        [3, 2, 0]
        [6, 1, 5]
        [7, 4, 8]
 

  Move :  RIGHT > 
        [3, 0, 2]
        [6, 1, 5]
        [7, 4, 8]
 

  Move :  UP /\  
        [3, 1, 2]
        [6, 0, 5]
        [7, 4, 8]
 

  Move :  UP /\  
        [3, 1, 2]
        [6, 4, 5]
        [7, 0, 8]
 

  Move :  RIGHT > 
        [3, 1, 2]
        [6, 4, 5]
        [0, 7, 8]
 

  Move :  DOWN \/
        [3, 1, 2]
        [0, 4, 5]
        [6, 7, 8]
 

  Move :  DOWN \/
        [0, 1, 2]
        [3, 4, 5]
        [6, 7, 8]
 

                 => Goal State


------------------------------------------------------------


         Informed Search - Greedy Best First Search 

No. of states found        :  612
Depth Reached              :  65
No. of Moves to reach goal :  56

Path to reach Goal state:- 
  Move :  None
        [7, 2, 4]
        [5, 0, 6]
        [8, 3, 1]
 

  Move :  UP /\  
        [7, 2, 4]
        [5, 3, 6]
        [8, 0, 1]
 

  Move :  LEFT <  
        [7, 2, 4]
        [5, 3, 6]
        [8, 1, 0]
 

  Move :  DOWN \/
        [7, 2, 4]
        [5, 3, 0]
        [8, 1, 6]
 

  Move :  DOWN \/
        [7, 2, 0]
        [5, 3, 4]
        [8, 1, 6]
 

  Move :  RIGHT > 
        [7, 0, 2]
        [5, 3, 4]
        [8, 1, 6]
 

  Move :  RIGHT > 
        [0, 7, 2]
        [5, 3, 4]
        [8, 1, 6]
 

  Move :  UP /\  
        [5, 7, 2]
        [0, 3, 4]
        [8, 1, 6]
 

  Move :  LEFT <  
        [5, 7, 2]
        [3, 0, 4]
        [8, 1, 6]
 

  Move :  UP /\  
        [5, 7, 2]
        [3, 1, 4]
        [8, 0, 6]
 

  Move :  RIGHT > 
        [5, 7, 2]
        [3, 1, 4]
        [0, 8, 6]
 

  Move :  DOWN \/
        [5, 7, 2]
        [0, 1, 4]
        [3, 8, 6]
 

  Move :  DOWN \/
        [0, 7, 2]
        [5, 1, 4]
        [3, 8, 6]
 

  Move :  LEFT <  
        [7, 0, 2]
        [5, 1, 4]
        [3, 8, 6]
 

  Move :  UP /\  
        [7, 1, 2]
        [5, 0, 4]
        [3, 8, 6]
 

  Move :  RIGHT > 
        [7, 1, 2]
        [0, 5, 4]
        [3, 8, 6]
 

  Move :  UP /\  
        [7, 1, 2]
        [3, 5, 4]
        [0, 8, 6]
 

  Move :  LEFT <  
        [7, 1, 2]
        [3, 5, 4]
        [8, 0, 6]
 

  Move :  LEFT <  
        [7, 1, 2]
        [3, 5, 4]
        [8, 6, 0]
 

  Move :  DOWN \/
        [7, 1, 2]
        [3, 5, 0]
        [8, 6, 4]
 

  Move :  RIGHT > 
        [7, 1, 2]
        [3, 0, 5]
        [8, 6, 4]
 

  Move :  UP /\  
        [7, 1, 2]
        [3, 6, 5]
        [8, 0, 4]
 

  Move :  RIGHT > 
        [7, 1, 2]
        [3, 6, 5]
        [0, 8, 4]
 

  Move :  DOWN \/
        [7, 1, 2]
        [0, 6, 5]
        [3, 8, 4]
 

  Move :  LEFT <  
        [7, 1, 2]
        [6, 0, 5]
        [3, 8, 4]
 

  Move :  LEFT <  
        [7, 1, 2]
        [6, 5, 0]
        [3, 8, 4]
 

  Move :  UP /\  
        [7, 1, 2]
        [6, 5, 4]
        [3, 8, 0]
 

  Move :  RIGHT > 
        [7, 1, 2]
        [6, 5, 4]
        [3, 0, 8]
 

  Move :  RIGHT > 
        [7, 1, 2]
        [6, 5, 4]
        [0, 3, 8]
 

  Move :  DOWN \/
        [7, 1, 2]
        [0, 5, 4]
        [6, 3, 8]
 

  Move :  DOWN \/
        [0, 1, 2]
        [7, 5, 4]
        [6, 3, 8]
 

  Move :  LEFT <  
        [1, 0, 2]
        [7, 5, 4]
        [6, 3, 8]
 

  Move :  UP /\  
        [1, 5, 2]
        [7, 0, 4]
        [6, 3, 8]
 

  Move :  UP /\  
        [1, 5, 2]
        [7, 3, 4]
        [6, 0, 8]
 

  Move :  RIGHT > 
        [1, 5, 2]
        [7, 3, 4]
        [0, 6, 8]
 

  Move :  DOWN \/
        [1, 5, 2]
        [0, 3, 4]
        [7, 6, 8]
 

  Move :  LEFT <  
        [1, 5, 2]
        [3, 0, 4]
        [7, 6, 8]
 

  Move :  DOWN \/
        [1, 0, 2]
        [3, 5, 4]
        [7, 6, 8]
 

  Move :  RIGHT > 
        [0, 1, 2]
        [3, 5, 4]
        [7, 6, 8]
 

  Move :  UP /\  
        [3, 1, 2]
        [0, 5, 4]
        [7, 6, 8]
 

  Move :  LEFT <  
        [3, 1, 2]
        [5, 0, 4]
        [7, 6, 8]
 

  Move :  UP /\  
        [3, 1, 2]
        [5, 6, 4]
        [7, 0, 8]
 

  Move :  RIGHT > 
        [3, 1, 2]
        [5, 6, 4]
        [0, 7, 8]
 

  Move :  DOWN \/
        [3, 1, 2]
        [0, 6, 4]
        [5, 7, 8]
 

  Move :  LEFT <  
        [3, 1, 2]
        [6, 0, 4]
        [5, 7, 8]
 

  Move :  LEFT <  
        [3, 1, 2]
        [6, 4, 0]
        [5, 7, 8]
 

  Move :  UP /\  
        [3, 1, 2]
        [6, 4, 8]
        [5, 7, 0]
 

  Move :  RIGHT > 
        [3, 1, 2]
        [6, 4, 8]
        [5, 0, 7]
 

  Move :  RIGHT > 
        [3, 1, 2]
        [6, 4, 8]
        [0, 5, 7]
 

  Move :  DOWN \/
        [3, 1, 2]
        [0, 4, 8]
        [6, 5, 7]
 

  Move :  LEFT <  
        [3, 1, 2]
        [4, 0, 8]
        [6, 5, 7]
 

  Move :  UP /\  
        [3, 1, 2]
        [4, 5, 8]
        [6, 0, 7]
 

  Move :  LEFT <  
        [3, 1, 2]
        [4, 5, 8]
        [6, 7, 0]
 

  Move :  DOWN \/
        [3, 1, 2]
        [4, 5, 0]
        [6, 7, 8]
 

  Move :  RIGHT > 
        [3, 1, 2]
        [4, 0, 5]
        [6, 7, 8]
 

  Move :  RIGHT > 
        [3, 1, 2]
        [0, 4, 5]
        [6, 7, 8]
 

  Move :  DOWN \/
        [0, 1, 2]
        [3, 4, 5]
        [6, 7, 8]
 

                 => Goal State


------------------------------------------------------------


         Informed Search - A* Search 

No. of states found        :  6172
Depth Reached              :  26
No. of Moves to reach goal :  26

Path to reach Goal state:- 
  Move :  None
        [7, 2, 4]
        [5, 0, 6]
        [8, 3, 1]
 

  Move :  RIGHT > 
        [7, 2, 4]
        [0, 5, 6]
        [8, 3, 1]
 

  Move :  DOWN \/
        [0, 2, 4]
        [7, 5, 6]
        [8, 3, 1]
 

  Move :  LEFT <  
        [2, 0, 4]
        [7, 5, 6]
        [8, 3, 1]
 

  Move :  UP /\  
        [2, 5, 4]
        [7, 0, 6]
        [8, 3, 1]
 

  Move :  UP /\  
        [2, 5, 4]
        [7, 3, 6]
        [8, 0, 1]
 

  Move :  RIGHT > 
        [2, 5, 4]
        [7, 3, 6]
        [0, 8, 1]
 

  Move :  DOWN \/
        [2, 5, 4]
        [0, 3, 6]
        [7, 8, 1]
 

  Move :  LEFT <  
        [2, 5, 4]
        [3, 0, 6]
        [7, 8, 1]
 

  Move :  LEFT <  
        [2, 5, 4]
        [3, 6, 0]
        [7, 8, 1]
 

  Move :  DOWN \/
        [2, 5, 0]
        [3, 6, 4]
        [7, 8, 1]
 

  Move :  RIGHT > 
        [2, 0, 5]
        [3, 6, 4]
        [7, 8, 1]
 

  Move :  RIGHT > 
        [0, 2, 5]
        [3, 6, 4]
        [7, 8, 1]
 

  Move :  UP /\  
        [3, 2, 5]
        [0, 6, 4]
        [7, 8, 1]
 

  Move :  LEFT <  
        [3, 2, 5]
        [6, 0, 4]
        [7, 8, 1]
 

  Move :  LEFT <  
        [3, 2, 5]
        [6, 4, 0]
        [7, 8, 1]
 

  Move :  UP /\  
        [3, 2, 5]
        [6, 4, 1]
        [7, 8, 0]
 

  Move :  RIGHT > 
        [3, 2, 5]
        [6, 4, 1]
        [7, 0, 8]
 

  Move :  DOWN \/
        [3, 2, 5]
        [6, 0, 1]
        [7, 4, 8]
 

  Move :  LEFT <  
        [3, 2, 5]
        [6, 1, 0]
        [7, 4, 8]
 

  Move :  DOWN \/
        [3, 2, 0]
        [6, 1, 5]
        [7, 4, 8]
 

  Move :  RIGHT > 
        [3, 0, 2]
        [6, 1, 5]
        [7, 4, 8]
 

  Move :  UP /\  
        [3, 1, 2]
        [6, 0, 5]
        [7, 4, 8]
 

  Move :  UP /\  
        [3, 1, 2]
        [6, 4, 5]
        [7, 0, 8]
 

  Move :  RIGHT > 
        [3, 1, 2]
        [6, 4, 5]
        [0, 7, 8]
 

  Move :  DOWN \/
        [3, 1, 2]
        [0, 4, 5]
        [6, 7, 8]
 

  Move :  DOWN \/
        [0, 1, 2]
        [3, 4, 5]
        [6, 7, 8]
 

                 => Goal State


------------------------------------------------------------

'''