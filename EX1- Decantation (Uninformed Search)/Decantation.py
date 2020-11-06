import math
import random
# constants 
no_of_jars = 3
target = 4

capacity = (8, 5, 3)
current = (8, 0, 0)

#variables 
target_list = []
queue_states = []
visited_states = []
explored_states = dict()
parent = dict()

def clear():
  global target_list, queue_states, visited_states, explored_states, parent
  target_list = []
  queue_states = []
  visited_states = []
  explored_states = dict()
  parent = dict()


#functions
def decant(i, j, a):  #tries to empty ith jar into jth one
    current = list(a)
    if(current[i] + current[j] >= capacity[j]):
      total = current[i] + current[j]
      current[j] = capacity[j]
      current[i] = total - current[j]
    else:
      current[j] += current[i]
      current[i] = 0

    return tuple(current)
    
def nextStates(current): #generates a set of unvisited next states from a current state
    next_states = []
    for i in range(no_of_jars):
        for j in range(no_of_jars):
            if (i != j and current[i] != 0 and current[j] != capacity[j]):
              new_state = decant(i, j, current)
              next_states.append(new_state)
    random.shuffle(next_states)
    return next_states

def isTargetFound(current): #checks if the target is achieved
  if target in current:
    return True
  else:
    return False


def BFStraversal():  #trverses the whole graph (state space here ) only once
  clear()
  global queue_states
  print("The order of explored states : ")

  queue_states.append(current)
  visited_states.append(current)
  
  parent[current] = current
  while(len(queue_states) > 0):
    current_state = queue_states[0]
    
    if(isTargetFound(current_state)):
      target_list.append(current_state)
    
    next_states = nextStates(current_state)
    #queue_states = queue_states + next_states
    
    for node in next_states:
          if node not in visited_states:
                queue_states.append(node)
                parent[node] = current_state
                visited_states.append(node)
    
    explored_states[current_state] = True
    print("\t-> ", current_state)
    queue_states.pop(0)
    
  print()

def DFS(node, Parent = current, depth = 0, maxDepth = math.inf):
      if(depth == maxDepth):
          return None
        
      global visited_states
      parent[node] = Parent
      visited_states.append(node)
      
      print("\t-> ", node)
    
      if(isTargetFound(node)):
            target_list.append(node)
      
      for nextNode in nextStates(node):
            if nextNode not in visited_states:
              DFS(nextNode, node, depth+1, maxDepth)

def DFStraversal():
    clear()
    
    global visited_states
    print("The order of explored states : ")
    
    parent[current] = current
    DFS(current)

def DLStraversal():
      depth = 1
      print("The order of explored states : ")
    
      while(True):
            clear()
            print('\nDEPTH ', depth, ' : ')
            DFS(current, maxDepth=depth)
            
            if(target_list):
                  return None
            depth+=1

def printPath(string):   #prints path of every possible final states
  print("\nThe List of Possible target State(s) is(are) : ", end="")
  print(target_list)
  print()
  for psbl_target in target_list: 
    ans = []
    ans.append(psbl_target)
    temp = psbl_target
    
    while(parent[temp]!=temp):
      ans.append(parent[temp])
      temp = parent[temp]
    
    print("Path to reach ",psbl_target, " : ", end = "")
    ans = ans[::-1]

    print(ans[0], end= "")
    for i in range(1,len(ans)):
      print(" -> ",ans[i],end="")
    print()

  print()
  print("No. of states visited by ",string,": ", len(visited_states))
  print("The states are : ", end="")
  
  print(visited_states[0],end = "")
  for i in range(1,len(visited_states)):
    print(", ",visited_states[i],end="")
  print()

if __name__  == "__main__":
  print("\t\tDecantation Problem")
  print("\t\t~~~~~~~~~~~ ~~~~~~~")
  
  print('\n---------------------------------------------------\n')
  
  print("** Breath First Search **\n")
  BFStraversal()  
  printPath("BFS")
  
  print('\n---------------------------------------------------\n')
  
  print("\n** Depth First Search **\n")
  DFStraversal()
  printPath("DFS")
  
  print('\n---------------------------------------------------\n')
  
  print("\n** Depth Limited Search **\n")
  DLStraversal()
  printPath("DLS")
  
  print('\n---------------------------------------------------\n')
  

'''
OUTPUT:
                Decantation Problem
                ~~~~~~~~~~~ ~~~~~~~

---------------------------------------------------

** Breath First Search **

The order of explored states : 
        ->  (8, 0, 0)
        ->  (3, 5, 0)
        ->  (5, 0, 3)
        ->  (0, 5, 3)
        ->  (3, 2, 3)
        ->  (5, 3, 0)
        ->  (6, 2, 0)
        ->  (2, 3, 3)
        ->  (6, 0, 2)
        ->  (2, 5, 1)
        ->  (1, 5, 2)
        ->  (7, 0, 1)
        ->  (1, 4, 3)
        ->  (7, 1, 0)
        ->  (4, 4, 0)
        ->  (4, 1, 3)


The List of Possible target State(s) is(are) : [(1, 4, 3), (4, 4, 0), (4, 1, 3)]

Path to reach  (1, 4, 3)  : (8, 0, 0) ->  (3, 5, 0) ->  (3, 2, 3) ->  (6, 2, 0) ->  (6, 0, 2) ->  (1, 5, 2) ->  (1, 4, 3)
Path to reach  (4, 4, 0)  : (8, 0, 0) ->  (3, 5, 0) ->  (3, 2, 3) ->  (6, 2, 0) ->  (6, 0, 2) ->  (1, 5, 2) ->  (1, 4, 3) ->  (4, 4, 0)
Path to reach  (4, 1, 3)  : (8, 0, 0) ->  (5, 0, 3) ->  (5, 3, 0) ->  (2, 3, 3) ->  (2, 5, 1) ->  (7, 0, 1) ->  (7, 1, 0) ->  (4, 1, 3)

No. of states visited by  BFS :  16
The states are : (8, 0, 0),  (3, 5, 0),  (5, 0, 3),  (0, 5, 3),  (3, 2, 3),  (5, 3, 0),  (6, 2, 0),  (2, 3, 3),  (6, 0, 2),  (2, 5, 1),  (1, 5, 2),  (7, 0, 1),  (1, 4, 3),  (7, 1, 0),  (4, 4, 0),  (4, 1, 3)

---------------------------------------------------


** Depth First Search **

The order of explored states : 
        ->  (8, 0, 0)
        ->  (3, 5, 0)
        ->  (0, 5, 3)
        ->  (5, 0, 3)
        ->  (5, 3, 0)
        ->  (2, 3, 3)
        ->  (2, 5, 1)
        ->  (7, 0, 1)
        ->  (7, 1, 0)
        ->  (4, 1, 3)
        ->  (4, 4, 0)
        ->  (1, 4, 3)
        ->  (1, 5, 2)
        ->  (6, 0, 2)
        ->  (6, 2, 0)
        ->  (3, 2, 3)

The List of Possible target State(s) is(are) : [(4, 1, 3), (4, 4, 0), (1, 4, 3)]

Path to reach  (4, 1, 3)  : (8, 0, 0) ->  (3, 5, 0) ->  (0, 5, 3) ->  (5, 0, 3) ->  (5, 3, 0) ->  (2, 3, 3) ->  (2, 5, 1) ->  (7, 0, 1) ->  (7, 1, 0) ->  (4, 1, 3)
Path to reach  (4, 4, 0)  : (8, 0, 0) ->  (3, 5, 0) ->  (0, 5, 3) ->  (5, 0, 3) ->  (5, 3, 0) ->  (2, 3, 3) ->  (2, 5, 1) ->  (7, 0, 1) ->  (7, 1, 0) ->  (4, 1, 3) ->  (4, 4, 0)
Path to reach  (1, 4, 3)  : (8, 0, 0) ->  (3, 5, 0) ->  (0, 5, 3) ->  (5, 0, 3) ->  (5, 3, 0) ->  (2, 3, 3) ->  (2, 5, 1) ->  (7, 0, 1) ->  (7, 1, 0) ->  (4, 1, 3) ->  (4, 4, 0) ->  (1, 4, 3)

No. of states visited by  DFS :  16
The states are : (8, 0, 0),  (3, 5, 0),  (0, 5, 3),  (5, 0, 3),  (5, 3, 0),  (2, 3, 3),  (2, 5, 1),  (7, 0, 1),  (7, 1, 0),  (4, 1, 3),  (4, 4, 0),  (1, 4, 3),  (1, 5, 2),  (6, 0, 2),  (6, 2, 0),  (3, 2, 3)

---------------------------------------------------


** Depth Limited Search **

The order of explored states : 

DEPTH  1  : 
        ->  (8, 0, 0)

DEPTH  2  : 
        ->  (8, 0, 0)
        ->  (3, 5, 0)
        ->  (5, 0, 3)

DEPTH  3  : 
        ->  (8, 0, 0)
        ->  (3, 5, 0)
        ->  (0, 5, 3)
        ->  (3, 2, 3)
        ->  (5, 0, 3)
        ->  (5, 3, 0)

DEPTH  4  : 
        ->  (8, 0, 0)
        ->  (3, 5, 0)
        ->  (0, 5, 3)
        ->  (5, 0, 3)
        ->  (3, 2, 3)
        ->  (6, 2, 0)

DEPTH  5  : 
        ->  (8, 0, 0)
        ->  (3, 5, 0)
        ->  (0, 5, 3)
        ->  (5, 0, 3)
        ->  (5, 3, 0)
        ->  (3, 2, 3)
        ->  (6, 2, 0)
        ->  (6, 0, 2)

DEPTH  6  : 
        ->  (8, 0, 0)
        ->  (3, 5, 0)
        ->  (0, 5, 3)
        ->  (5, 0, 3)
        ->  (5, 3, 0)
        ->  (2, 3, 3)
        ->  (3, 2, 3)
        ->  (6, 2, 0)
        ->  (6, 0, 2)
        ->  (1, 5, 2)

DEPTH  7  : 
        ->  (8, 0, 0)
        ->  (3, 5, 0)
        ->  (0, 5, 3)
        ->  (5, 0, 3)
        ->  (5, 3, 0)
        ->  (2, 3, 3)
        ->  (2, 5, 1)
        ->  (3, 2, 3)
        ->  (6, 2, 0)
        ->  (6, 0, 2)
        ->  (1, 5, 2)
        ->  (1, 4, 3)

The List of Possible target State(s) is(are) : [(1, 4, 3)]

Path to reach  (1, 4, 3)  : (8, 0, 0) ->  (3, 5, 0) ->  (3, 2, 3) ->  (6, 2, 0) ->  (6, 0, 2) ->  (1, 5, 2) ->  (1, 4, 3)

No. of states visited by  DLS :  12
The states are : (8, 0, 0),  (3, 5, 0),  (0, 5, 3),  (5, 0, 3),  (5, 3, 0),  (2, 3, 3),  (2, 5, 1),  (3, 2, 3),  (6, 2, 0),  (6, 0, 2),  (1, 5, 2),  (1, 4, 3)

---------------------------------------------------

'''