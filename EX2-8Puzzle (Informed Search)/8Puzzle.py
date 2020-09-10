# constants 
#import sys
#sys.stdout = open("states.txt","w")

initial_board = ((7,2,4), (5,0,6) , (8,3,1));
final_board = ((0,1,2), (3,4,5), (6,7,8));
#initial_board = ((1,2,3),(4,5,6),(7,8,0));
#final_board = ((0,1,3),(4,2,5),(7,8,6));
row = 3
col = 3

#variables 
queue_states = []
visited_states = set()
explored_states = dict()
parent = dict()

#functions
def left(x,y):
      if(y-1 < 0):
            return (-1,-1)
      return (x,y-1)

def right(x,y):
      if(y+1 == col):
            return (-1,-1)
      return (x,y+1)

def up(x,y):
      if(x-1 < 0):
            return (-1,-1)
      return (x-1,y)

def down(x,y):
      if(x+1 == row):
            return (-1,-1)
      return (x+1,y)


def nextStates(current): #generates a set of unvisited next states from a current state
    global visited_states, parent
    next_states = []
    #finding coord of 0 - empty slot
    x,y = -1,-1
    
    for i in range(row):
          for j in range(col):
                if(current[i][j] == 0):
                      x,y = i,j;
                      break
          if(x != -1):
                break
    
    #move left element here if present
    newx,newy = left(x,y)
    if(newx!=-1):
          a = []
          for tupl in current:
            a.append(list(tupl))
          a[x][y] , a[newx][newy] = a[newx][newy], a[x][y]
          b = []
          for lis in a:
                b.append(tuple(lis))
          b = tuple(b)
          if(b not in visited_states):
            next_states.append(b)
            visited_states.add(b)
            parent[b] = current
    
    
    #move right element here if present
    newx,newy = right(x,y)
    if(newx!=-1):
          a = []
          for tupl in current:
            a.append(list(tupl))
          a[x][y] , a[newx][newy] = a[newx][newy], a[x][y]
          b = []
          for lis in a:
                b.append(tuple(lis))
          b = tuple(b)
          if(b not in visited_states):
            next_states.append(b)
            visited_states.add(b)
            parent[b] = current
    
    #move above element here if present
    newx,newy = up(x,y)
    if(newx!=-1):
          a = []
          for tupl in current:
            a.append(list(tupl))
          a[x][y] , a[newx][newy] = a[newx][newy], a[x][y]
          b = []
          for lis in a:
                b.append(tuple(lis))
          b = tuple(b)
          if(b not in visited_states ):
            next_states.append(b)
            visited_states.add(b)
            parent[b] = current
    
    #move below element here if present
    newx,newy = down(x,y)
    if(newx!=-1):
          a = []
          for tupl in current:
            a.append(list(tupl))
          a[x][y] , a[newx][newy] = a[newx][newy], a[x][y]
          b = []
          for lis in a:
                b.append(tuple(lis))
          b = tuple(b)
          if(b not in visited_states):
            next_states.append(b)
            visited_states.add(b)
            parent[b] = current
    
    return next_states
    
def isTargetFound(current): #checks if the target is achieved
  if current == final_board:
    return True
  else:
    return False


def BFStraversal():  #trverses the whole graph (state space here ) only once
  global queue_states, visited_states, parent, explored_states
  #print("The order of explored states : ")

  queue_states.append(initial_board)
  visited_states.add(initial_board)
  
  parent[initial_board] = initial_board
  
  while(len(queue_states) > 0):
        
    current_state = queue_states.pop(0)
          
    if(isTargetFound(current_state)):
          break
    
    next_states = nextStates(current_state)
    
    queue_states = queue_states + next_states
    explored_states[current_state] = True
    #print("\t-> ", current_state)
    
   
def printPath():   #prints path of every possible final states
      ans = []
      ans.append(final_board)
      temp = final_board
      
      print("No. of states visited by BFS: ", len(visited_states))
      
      
      while(temp in parent and parent[temp]!=temp):
            ans.append(parent[temp])
            temp = parent[temp]

      print("\nPath length to reach the goal state : ",len(ans),"\n");
      print("Path to reach the goal state : ", end = "\n")
      ans = ans[::-1]

      for i in range(len(ans)):
            cou = 0
            for k in ans[i]:
                  if(cou == 0):
                        print("\t-> ",list(k))
                        cou = 1
                  else:
                        print("\t   ",list(k))
            print()

      print("\t\t => Goal State reached\n")
      
      
      #print("The states are : ", end="")
  
      # print(visited_states[0],end = "")
      # for i in range(1,len(visited_states)):
      #       print(", ",visited_states[i],end="")
      # print()

def main():
  print("\t\t8-Puzzle Problem\n")
  BFStraversal()  
  printPath()

main()

'''
OUTPUT @4:35pm using bfs

                8-Puzzle Problem


No. of states visited by BFS:  175326

Path length to reach the goal state :  27 

Path to reach the goal state : 
        ->  [7, 2, 4]
            [5, 0, 6]
            [8, 3, 1]

        ->  [7, 2, 4]
            [0, 5, 6]
            [8, 3, 1]

        ->  [0, 2, 4]
            [7, 5, 6]
            [8, 3, 1]

        ->  [2, 0, 4]
            [7, 5, 6]
            [8, 3, 1]

        ->  [2, 5, 4]
            [7, 0, 6]
            [8, 3, 1]

        ->  [2, 5, 4]
            [7, 6, 0]
            [8, 3, 1]

        ->  [2, 5, 4]
            [7, 6, 1]
            [8, 3, 0]

        ->  [2, 5, 4]
            [7, 6, 1]
            [8, 0, 3]

        ->  [2, 5, 4]
            [7, 6, 1]
            [0, 8, 3]

        ->  [2, 5, 4]
            [0, 6, 1]
            [7, 8, 3]

        ->  [2, 5, 4]
            [6, 0, 1]
            [7, 8, 3]

        ->  [2, 5, 4]
            [6, 1, 0]
            [7, 8, 3]

        ->  [2, 5, 4]
            [6, 1, 3]
            [7, 8, 0]

        ->  [2, 5, 4]
            [6, 1, 3]
            [7, 0, 8]

        ->  [2, 5, 4]
            [6, 1, 3]
            [0, 7, 8]

        ->  [2, 5, 4]
            [0, 1, 3]
            [6, 7, 8]

        ->  [2, 5, 4]
            [1, 0, 3]
            [6, 7, 8]

        ->  [2, 5, 4]
            [1, 3, 0]
            [6, 7, 8]

        ->  [2, 5, 0]
            [1, 3, 4]
            [6, 7, 8]

        ->  [2, 0, 5]
            [1, 3, 4]
            [6, 7, 8]

        ->  [0, 2, 5]
            [1, 3, 4]
            [6, 7, 8]

        ->  [1, 2, 5]
            [0, 3, 4]
            [6, 7, 8]

        ->  [1, 2, 5]
            [3, 0, 4]
            [6, 7, 8]

        ->  [1, 2, 5]
            [3, 4, 0]
            [6, 7, 8]

        ->  [1, 2, 0]
            [3, 4, 5]
            [6, 7, 8]

        ->  [1, 0, 2]
            [3, 4, 5]
            [6, 7, 8]

        ->  [0, 1, 2]
            [3, 4, 5]
            [6, 7, 8]

                 => Goal State reached

'''

'''
OUTPUT @4:04pm using Bfs - uninformed search

                8-Puzzle Problem

Path to reach  ((0, 1, 2), (3, 4, 5), (6, 7, 8))  : 
        ->  ((7, 2, 4), (5, 0, 6), (8, 3, 1))
        ->  ((7, 2, 4), (0, 5, 6), (8, 3, 1))
        ->  ((0, 2, 4), (7, 5, 6), (8, 3, 1))
        ->  ((2, 0, 4), (7, 5, 6), (8, 3, 1))
        ->  ((2, 5, 4), (7, 0, 6), (8, 3, 1))
        ->  ((2, 5, 4), (7, 6, 0), (8, 3, 1))
        ->  ((2, 5, 4), (7, 6, 1), (8, 3, 0))
        ->  ((2, 5, 4), (7, 6, 1), (8, 0, 3))
        ->  ((2, 5, 4), (7, 6, 1), (0, 8, 3))
        ->  ((2, 5, 4), (0, 6, 1), (7, 8, 3))
        ->  ((2, 5, 4), (6, 0, 1), (7, 8, 3))
        ->  ((2, 5, 4), (6, 1, 0), (7, 8, 3))
        ->  ((2, 5, 4), (6, 1, 3), (7, 8, 0))
        ->  ((2, 5, 4), (6, 1, 3), (7, 0, 8))
        ->  ((2, 5, 4), (6, 1, 3), (0, 7, 8))
        ->  ((2, 5, 4), (0, 1, 3), (6, 7, 8))
        ->  ((2, 5, 4), (1, 0, 3), (6, 7, 8))
        ->  ((2, 5, 4), (1, 3, 0), (6, 7, 8))
        ->  ((2, 5, 0), (1, 3, 4), (6, 7, 8))
        ->  ((2, 0, 5), (1, 3, 4), (6, 7, 8))
        ->  ((0, 2, 5), (1, 3, 4), (6, 7, 8))
        ->  ((1, 2, 5), (0, 3, 4), (6, 7, 8))
        ->  ((1, 2, 5), (3, 0, 4), (6, 7, 8))
        ->  ((1, 2, 5), (3, 4, 0), (6, 7, 8))
        ->  ((1, 2, 0), (3, 4, 5), (6, 7, 8))
        ->  ((1, 0, 2), (3, 4, 5), (6, 7, 8))
        ->  ((0, 1, 2), (3, 4, 5), (6, 7, 8))


No. of states visited by BFS:  175326

'''


