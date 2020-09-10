import math
import matplotlib.pyplot as plt
import random

def manhattan_distance(A,B):
    '''
    Calculates and returns the manhattan distance between two giiven points
    '''
    
    return abs(A[0]-B[0])+abs(A[1]-B[1])

def calc_distance(Point, SetOfPoints):
    '''
    Calculates the sum of Manhattan Distances of a given point 
    from the given set of points
    '''
    
    sum = 0
    
    for border_pt in SetOfPoints:
        sum += manhattan_distance(Point, border_pt)
    
    return sum

def compliment(move):
    '''
    Return the opposite of the move made
    if the move was up [(0,1)] it returns down [(0,-1)] 
    if the move was right [(1,0)] it returns left [(-1,0)] 
    and vice versa 
    '''
    
    return (-move[0], -move[1])

def Hill_Climber(Points, Expected_Centre, last_move = (0,0)):
    '''
    Climbs up the Hill to find a local optimum value. 
    When a more optimum value is not found, We conclude that the 
    current state(cur_board) to be the local optimum value  
    '''
    
    direction = [(0,-1),(1,0),(-1,0),(0,1)]  #equi to [down, right, left, up]
    
    min_pt = Expected_Centre
    min_dist = calc_distance(Expected_Centre, Points)

    for move in direction:
        dx = move[0]
        dy = move[1]
        dist = calc_distance((Expected_Centre[0]+dx, Expected_Centre[1]+dy),Points)
        
        if(dist < min_dist):
            min_dist = dist
            min_pt = (Expected_Centre[0]+dx, Expected_Centre[1]+dy);   
            last_move = move  
        elif(dist == min_dist and move != compliment(last_move)):
            min_pt = (Expected_Centre[0]+dx, Expected_Centre[1]+dy);     
            last_move = move
    
    if(min_pt == Expected_Centre):
        return Expected_Centre
    
    return Hill_Climber(Points, min_pt, last_move)


if __name__ == "__main__":
    print("\t\t    Hill Climbing \n\t\tCentre of Set of Points\n")

    Points = [(0,6),(1,2),(3,1),(7,0),(9,3)]
    
    #Assuming a random Centre
    X,Y = random.randint(-10,10),random.randint(-10,10)

    #uncomment this part to start from an Approximate centre
    # X,Y = 0,0
    # for x,y in Points:
    #     X+=x;
    #     Y+=y;
    # X//=len(Points)
    # Y//=len(Points)

    xs = [x[0] for x in Points]
    ys = [x[1] for x in Points]
    
    Expected_Centre = (X,Y)
    Expected_Centre_x = [Expected_Centre[0]]
    Expected_Centre_y = [Expected_Centre[1]]
    
    print("Border Points of Assumed Circle : ", Points);
    print()

    print("Assumed Centre         : ",Expected_Centre);
    print("Initial Manhattan Dist : ",calc_distance(Expected_Centre, Points));
    print()

    Centre = Hill_Climber(Points, Expected_Centre)
    Centre_x = [Centre[0]]
    Centre_y = [Centre[1]]
    
    print("Final Centre           : ",Centre);
    print("Final Manhattan Dist   : ",calc_distance(Centre, Points));
    print()

    #- comment these lines if you dont want the plot
    plt.scatter(xs,ys,color = "black",label="Border Points")
    plt.scatter(Expected_Centre_x, Expected_Centre_y, color = "red", label="Assumed Centre")
    plt.scatter(Centre_x, Centre_y, color = "green", label="Approx. Final Centre")
    plt.legend()
    plt.show()
    
'''
Output @14.30 : 
                    Hill Climbing 
                Centre of Set of Points

Border Points of Assumed Circle :  [(0, 6), (1, 2), (3, 1), (7, 0), (9, 3)]

Assumed Centre         :  (2, -7)
Initial Manhattan Dist :  63

Final Centre           :  (3, 2)
Final Manhattan Dist   :  23

## -> A scatter plot will pop out to show the points in its place
'''