import math
import random
from copy import deepcopy
from collections import deque

# 
# -> M refers to missionaries
# -> C refers to Cannibals
# -> B refers to boat 

# M_L -> No. of Missionaries on left side
# M_R -> No. of Missionaries on right side
# C_L -> No. of Cannibals on left side
# C_R -> No. of Cannibals on right side
# B = 'L' -> Boat on left bank
# B = 'R' -> Boat on right bank


M_L = 0
M_R = 1
C_L = 2
C_R = 3
B = 4

class State:
     
    def __init__(self, state):
        
        
        self.state = state
        self.M = state[M_L] + state[M_R]
        self.C = state[C_L] + state[C_R]
        self.parent = None
    
    def __str__(self):
        
        string = ""
        string += '\t' + ('  ' * (self.M - self.state[M_L])) + ('M ' * (self.state[M_L])) + '|'
        if self.state[B] == 'L':
            string += ' B ~ ~ ~ '
        else:
            string += ' ~ ~ ~ B '
        string += '|' + ('M ' * (self.state[M_R])) + '\n'
        
        string += '\t' + ('  ' * (self.C - self.state[C_L])) + ('C ' * (self.state[C_L])) + '|'
        string += ' ~ ~ ~ ~ '
        string += '|' + ('C ' * (self.state[C_R])) + '\n'
        
        return string
        
    def isValidState(self):

        if self.state[C_L] < 0 or self.state[C_R] < 0 or self.state[M_L] < 0 or self.state[M_R] < 0:
            return False
        if (self.state[C_L] > self.state[M_L] and self.state[M_L] > 0) or (self.state[C_R] > self.state[M_R] and self.state[M_R] > 0):
            return False
        return True
    
    def isGoalState(self):
        if  self.isValidState() and \
            self.M == self.state[M_R] and self.state[M_L] == 0 and \
            self.C == self.state[C_R] and self.state[C_L] == 0 and \
            self.state[B] == 'R' :
                return True
        return False
    
    def nextStates(self):
    
        next_states = []
        
        
        if self.state[B] == 'L':
            for i in range(1,3):
                new_state = deepcopy(self.state)
                new_state[M_L] -= i
                new_state[M_R] += i
                new_state[B] = 'R'
                
                new_state = State(new_state)
                if new_state.isValidState():
                    next_states.append(new_state)
                
                new_state = deepcopy(self.state)
                new_state[C_L] -= i
                new_state[C_R] += i
                new_state[B] = 'R'
                
                new_state = State(new_state)
               # print(new_state)
                if new_state.isValidState():
                    next_states.append(new_state)
                
            new_state = deepcopy(self.state)
            new_state[M_L] -= 1
            new_state[M_R] += 1
            new_state[C_L] -= 1
            new_state[C_R] += 1
            new_state[B] = 'R'
            
            new_state = State(new_state)
            if new_state.isValidState():
                next_states.append(new_state)
                
            
        else:
            for i in range(1,3):
                new_state = deepcopy(self.state)
                new_state[M_R] -= i
                new_state[M_L] += i
                new_state[B] = 'L'
                
                new_state = State(new_state)
                if new_state.isValidState():
                    next_states.append(new_state)
                
                new_state = deepcopy(self.state)
                new_state[C_R] -= i
                new_state[C_L] += i
                new_state[B] = 'L'
                
                new_state = State(new_state)
                if new_state.isValidState():
                    next_states.append(new_state)
                
            new_state = deepcopy(self.state)
            new_state[M_R] -= 1
            new_state[M_L] += 1
            new_state[C_R] -= 1
            new_state[C_L] += 1
            new_state[B] = 'L'
            
            new_state = State(new_state)
            if new_state.isValidState():
                next_states.append(new_state)
        
        random.shuffle(next_states)
        
        return next_states

class Solver:
    
    def setPath(self, goal):
        start = goal
        path = []
        while start:
            path.append(start)
            start = start.parent
        
        return path[::-1]
    
    def BFS(self, state):

        frontier = deque()
        visited_states = set()
        
        print('The order of explored states are : ')
        
        visited_states.add(tuple(state.state))
        frontier.append(state)
        
        while frontier:    
            current_state = frontier.popleft()
            
            print('\t-> ', current_state.state)
            
            if current_state.isGoalState():
                print()
                return current_state, self.setPath(goal = current_state)
            
            for next_state in current_state.nextStates():
                if tuple(next_state.state) not in visited_states:
                    frontier.append(next_state)
                    next_state.parent = current_state
                    visited_states.add(tuple(next_state.state))
        print()
        return None, None

    def printPath(self, path):
        
        print('The sequence through which the goal is achieved is : ')
        print('Start :- ')
        
        for i,state in enumerate(path):
            print(state)
            
            if(i == len(path)-1):
                print('\t\t  => Goal State Reached\n')
            else:
                print('  ---> ')

if __name__ == "__main__":
    
    print('\n\t\t + Missionaries and Cannibals x ')
    print('\n--------------------------------------------\n')
    state = ['-' for i in range(5)]
    state[M_L], state[C_L], state[M_R], state[C_R], state[B] = 3, 3, 0, 0, 'L'
    
    initial_state = State(state = state)
    
    print('Initial State : ')
    print(initial_state)
    
    print('\n--------------------------------------------\n')
    
    Sol = Solver()
    print('** Breath First Search **\n')
    goal, path = Sol.BFS(state = initial_state)
    
    if goal:
        Sol.printPath(path = path)
    else:
        print('Goal Not found !!!')
    
    print('\n--------------------------------------------\n')


'''
OUTPUT :

                 + Missionaries and Cannibals x 

--------------------------------------------

Initial State : 
        M M M | B ~ ~ ~ |
        C C C | ~ ~ ~ ~ |


--------------------------------------------

** Breath First Search **

The order of explored states are : 
        ->  [3, 0, 3, 0, 'L']
        ->  [3, 0, 2, 1, 'R']
        ->  [3, 0, 1, 2, 'R']
        ->  [2, 1, 2, 1, 'R']
        ->  [3, 0, 2, 1, 'L']
        ->  [3, 0, 0, 3, 'R']
        ->  [3, 0, 1, 2, 'L']
        ->  [1, 2, 1, 2, 'R']
        ->  [2, 1, 2, 1, 'L']
        ->  [0, 3, 2, 1, 'R']
        ->  [0, 3, 3, 0, 'L']
        ->  [0, 3, 1, 2, 'R']
        ->  [0, 3, 2, 1, 'L']
        ->  [1, 2, 1, 2, 'L']
        ->  [0, 3, 0, 3, 'R']

The sequence through which the goal is achieved is : 
Start :- 
        M M M | B ~ ~ ~ |
        C C C | ~ ~ ~ ~ |

  ---> 
        M M M | ~ ~ ~ B |
            C | ~ ~ ~ ~ |C C 

  ---> 
        M M M | B ~ ~ ~ |
          C C | ~ ~ ~ ~ |C 

  ---> 
        M M M | ~ ~ ~ B |
              | ~ ~ ~ ~ |C C C 

  ---> 
        M M M | B ~ ~ ~ |
            C | ~ ~ ~ ~ |C C 

  ---> 
            M | ~ ~ ~ B |M M 
            C | ~ ~ ~ ~ |C C 

  ---> 
          M M | B ~ ~ ~ |M 
          C C | ~ ~ ~ ~ |C 

  ---> 
              | ~ ~ ~ B |M M M 
          C C | ~ ~ ~ ~ |C 

  ---> 
              | B ~ ~ ~ |M M M 
        C C C | ~ ~ ~ ~ |

  ---> 
              | ~ ~ ~ B |M M M 
            C | ~ ~ ~ ~ |C C 

  ---> 
              | B ~ ~ ~ |M M M 
          C C | ~ ~ ~ ~ |C 

  ---> 
              | ~ ~ ~ B |M M M 
              | ~ ~ ~ ~ |C C C 

                  => Goal State Reached


--------------------------------------------

'''