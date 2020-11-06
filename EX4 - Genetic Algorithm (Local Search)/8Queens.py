import random 
import math
import heapq

class Board_State:
    state = None
    fitness = math.inf
    size = 0;
    
    def __init__(self,state):
        '''
        Used to initialize the state with No of queens 
        and the conflicts btw them as fitness using fitness function
        '''
        
        self.state = state
        self.size = len(state)
        self.fitness = self.fitness_fn() # objective function
        
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
    
    def fitness_fn(self): #
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

class Genetic_Solver:
    '''
    function GENETIC -ALGORITHM ( population , FITNESS -FN ) returns an individual
        inputs: population , a set of individuals
                FITNESS-FN , a function that measures the fitness of an individual
    
        repeat
            new population ← empty set
            for i = 1 to SIZE ( population) do
                x ← RANDOM -SELECTION ( population, FITNESS-FN )
                y ← RANDOM -SELECTION ( population, FITNESS-FN )
                child ← REPRODUCE (x , y)
                if (small random probability) then child ← MUTATE (child )
                add child to new population
            population ← new population
        until some individual is fit enough, or enough time has elapsed
        return the best individual in population , according to FITNESS-FN
    
    
    function REPRODUCE (x , y) returns an individual
        inputs: x , y, parent individuals
        
        n ← LENGTH (x); c ← random number from 1 to n
        return APPEND (SUBSTRING (x , 1, c), SUBSTRING (y, c + 1, n))
    '''
    
    Converging_cnt  = 0
    Converged_board = None
    
    def __init__(self):
        '''
        Uses the genetic algorithm to solve N-queens problem.
        '''
        
        Converging_cnt  = 0
        Converged_board = None
     
    
    def select(self,board_population, best_count):
        '''
        Used to select Best best-count fitness valued boards from 
        the whole population 
        '''
        
        return board_population[:best_count]

    def mutationProbablity(self):
        '''
        return True with a probablity of 1/100, else return false
        '''
        
        probablity = 0.01
        return random.random() < probablity 
    
    def mutate(self,board):  
        '''
        Takes a random board from the population and changes 
        some postion in that board
        '''  
        randInd = random.randint(0,board.size-1)
        randPos = random.randint(1,board.size)
        
        new_board = list(board.state)
        new_board[randInd] = randPos
        
        return Board_State(new_board)

    def printProbablity(self):
        '''
        Print Generation value with a proabality of 10%
        '''
        
        probablity = 0.01
        return random.random() < probablity 
    
    def crossover(self,board_population, itr):
        '''
        Takes two boards among the best boards and slice them 
        Combine them to form children (basic crossover)
        
        Let the boards be X and Y
        ( ---> ) means sliced into 
        X --> A : B
        Y --> C : D
        
        now combine A : D and C : B
        and return 
        '''
        
        slicer  = random.randint(1,board_population[0].size-1)
        A = board_population[itr].state[:slicer]
        B = board_population[itr].state[slicer:]
        C = board_population[itr+1].state[:slicer]
        D = board_population[itr+1].state[slicer:]
        
        A += D
        C += B
        
        crossover_children = []
        crossover_children.append(Board_State(A))
        crossover_children.append(Board_State(C))
        
        return crossover_children   

    def GeneticConvergence(self,board_population, best_count, population_size):
        '''
        Converges the population untill a fully fit board is observed or a 
        iteration limit is reached
        
        Converges using mutation and crossover
        '''
        
        itr_cnt = 0
        max_itr = 1000
        itr_size = len(str(max_itr))
        
        while(itr_cnt < max_itr):
            board_population = self.select(board_population, best_count)
            next_population = []
            prev_best_board = board_population[0]
            
            for i in range(population_size):
                
                crossover_children = self.crossover(board_population,random.randint(0,best_count-2))
                
                if(self.mutationProbablity()):
                    child1 = self.mutate(crossover_children[0])
                    child2 = self.mutate(crossover_children[1])
                    crossover_children = []
                    crossover_children.append(child1)
                    crossover_children.append(child2)
                    
                next_population += crossover_children
            
            heapq.heapify(next_population)
            
            self.Converged_board = next_population[0]
            
            if(self.Converged_board.fitness == prev_best_board.size * (prev_best_board.size - 1) // 2):
                break

            if(self.Converged_board.fitness > prev_best_board.fitness):
                itr_cnt = 0
            else:
                itr_cnt += 1
            
            self.Converging_cnt += 1
            board_population = next_population            
            
            #print with a probablity
            if(self.printProbablity() or self.Converging_cnt == 1):
                print("Generation {0} - has a best child with fitness {1} ".format(str(self.Converging_cnt).zfill(itr_size), self.Converged_board.fitness))
            
        print()
            
    
if __name__ == "__main__":
    print("\t\tGenetic Algorithm\n\t\t N - Queens\n")
    population_size = 500
    K = min(population_size * 5//7, 50)
    board_length = 8
       
    board_population = []
    
    print("Generating Population ...\n")
    
    print("Generated about {0} samples\n".format(population_size))
    
    while len(board_population) < population_size:
        board = Board_State([random.randint(1,board_length) for i in range(board_length)])
        if(board.fitness < board_length*(board_length-1)//2 - board_length):
            heapq.heappush(board_population, board)   
    
    print("Converging .....\n")
    
    Final_Solution = Genetic_Solver()
    Final_Solution.GeneticConvergence(board_population, K , population_size) 
    
    print("Iterations took to converge to a Good state : ", Final_Solution.Converging_cnt)
    print()
    print("Final Board : ",Final_Solution.Converged_board)
    print("Fitness     : ", Final_Solution.Converged_board.fitness)
    print()


'''
Output :
                Genetic Algorithm
                 N - Queens

Generating Population ...

Generated about 500 samples

Converging .....

Generation 0001 - has a best child with fitness 27 
Generation 0116 - has a best child with fitness 27 
Generation 0117 - has a best child with fitness 27 
Generation 0365 - has a best child with fitness 27 
Generation 0391 - has a best child with fitness 27 
Generation 0515 - has a best child with fitness 27 
Generation 0649 - has a best child with fitness 27 
Generation 0845 - has a best child with fitness 27 
Generation 0853 - has a best child with fitness 27 
Generation 0856 - has a best child with fitness 27 
Generation 0881 - has a best child with fitness 27 
Generation 0988 - has a best child with fitness 27 

Iterations took to converge to a Good state :  1003

Final Board :  
        - - - - - - - Q 
        - - - Q - - - - 
        - - - - - - Q - 
        Q - - - - - - - 
        - - - - - Q - - 
        - Q - - - - - - 
        - - - - Q - - - 
        - - - - - - Q - 

Fitness     :  27

'''

'''
Output :
                Genetic Algorithm
                 N - Queens

Generating Population ...

Generated about 500 samples

Converging .....

Generation 0001 - has a best child with fitness 26 
Generation 0009 - has a best child with fitness 27 
Generation 0017 - has a best child with fitness 27 
Generation 0019 - has a best child with fitness 27 
Generation 0031 - has a best child with fitness 27 
Generation 0043 - has a best child with fitness 27 
Generation 0051 - has a best child with fitness 27 
Generation 0056 - has a best child with fitness 27 
Generation 0057 - has a best child with fitness 27 
Generation 0062 - has a best child with fitness 27 
Generation 0072 - has a best child with fitness 27 
Generation 0078 - has a best child with fitness 27 
Generation 0093 - has a best child with fitness 27 
Generation 0102 - has a best child with fitness 27 
Generation 0103 - has a best child with fitness 27 
Generation 0107 - has a best child with fitness 27 
Generation 0111 - has a best child with fitness 27 
Generation 0118 - has a best child with fitness 27 
Generation 0130 - has a best child with fitness 27 
Generation 0135 - has a best child with fitness 27 
Generation 0138 - has a best child with fitness 27 
Generation 0139 - has a best child with fitness 27 
Generation 0151 - has a best child with fitness 27 
Generation 0161 - has a best child with fitness 27 
Generation 0164 - has a best child with fitness 27 
Generation 0171 - has a best child with fitness 27 
Generation 0175 - has a best child with fitness 27 
Generation 0192 - has a best child with fitness 27 
Generation 0203 - has a best child with fitness 27 
Generation 0207 - has a best child with fitness 27 
Generation 0220 - has a best child with fitness 27 
Generation 0231 - has a best child with fitness 27 
Generation 0234 - has a best child with fitness 27 
Generation 0238 - has a best child with fitness 27 
Generation 0266 - has a best child with fitness 27 
Generation 0267 - has a best child with fitness 27 
Generation 0288 - has a best child with fitness 27 
Generation 0303 - has a best child with fitness 27 
Generation 0308 - has a best child with fitness 27 
Generation 0309 - has a best child with fitness 27 
Generation 0315 - has a best child with fitness 27 
Generation 0318 - has a best child with fitness 27 
Generation 0324 - has a best child with fitness 27 
Generation 0372 - has a best child with fitness 27 
Generation 0377 - has a best child with fitness 27 
Generation 0380 - has a best child with fitness 27 
Generation 0390 - has a best child with fitness 27 
Generation 0397 - has a best child with fitness 27 
Generation 0421 - has a best child with fitness 27 
Generation 0443 - has a best child with fitness 27 
Generation 0445 - has a best child with fitness 27 
Generation 0447 - has a best child with fitness 27 
Generation 0452 - has a best child with fitness 27 
Generation 0462 - has a best child with fitness 27 
Generation 0468 - has a best child with fitness 27 
Generation 0469 - has a best child with fitness 27 
Generation 0474 - has a best child with fitness 27 
Generation 0518 - has a best child with fitness 27 
Generation 0519 - has a best child with fitness 27 
Generation 0536 - has a best child with fitness 27 
Generation 0538 - has a best child with fitness 27 
Generation 0566 - has a best child with fitness 27 
Generation 0608 - has a best child with fitness 27 
Generation 0613 - has a best child with fitness 27 
Generation 0617 - has a best child with fitness 27 
Generation 0673 - has a best child with fitness 27 
Generation 0682 - has a best child with fitness 27 
Generation 0685 - has a best child with fitness 27 
Generation 0707 - has a best child with fitness 27 
Generation 0757 - has a best child with fitness 27 
Generation 0762 - has a best child with fitness 27 
Generation 0765 - has a best child with fitness 27 
Generation 0767 - has a best child with fitness 27 
Generation 0781 - has a best child with fitness 27 
Generation 0796 - has a best child with fitness 27 
Generation 0797 - has a best child with fitness 27 
Generation 0823 - has a best child with fitness 27 
Generation 0825 - has a best child with fitness 27 
Generation 0842 - has a best child with fitness 27 
Generation 0846 - has a best child with fitness 27 
Generation 0851 - has a best child with fitness 27 
Generation 0852 - has a best child with fitness 27 
Generation 0867 - has a best child with fitness 27 

Iterations took to converge to a Good state :  875

Final Board :  
        - - - - - Q - - 
        - - Q - - - - - 
        - - - - - - Q - 
        - - - Q - - - - 
        Q - - - - - - - 
        - - - - - - - Q 
        - Q - - - - - - 
        - - - - Q - - - 

Fitness     :  28

'''