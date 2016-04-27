import tanks
import ai

class Node:
	def __init__(self, playerTank, parent):
		self.playerTank = playerTank
		self.parent = parent
		self.H = 0
		self.G = 0
		
def children(parentNode):
	return self.playerTank.fakeMove()
	
def aStar(start, goal):
	obStart = Node(start, start)
	obGoal = Node(goal, goal)

    #The open and closed sets
	openset = set()
	closedset = set()
	
    #Current point is the starting point
	current = obStart
	
    #Add the starting point to the open set
	openset.add(current)
	
    #While the open set is not empty
	while openset:
	
        #Find the item in the open set with the lowest G + H score
		current = min(openset, key=lambda o:o.G + o.H)
		
        #If it is the item we want, retrace the path and return it
		if ObGoal.playerTank.collideEnemy:
			path = []
			while current.parent:
				path.append(current)
				current = current.parent
			path.append(current)
			return path[::-1]
			
        #Remove the item from the open set
		openset.remove(current)
		
        #Add it to the closed set
		closedset.add(current)
		
        #Loop through the node's children/siblings
		for node in children(current):
		
            #If it is already in the closed set, skip it
			if node in closedset:
				continue
				
            #Otherwise if it is already in the open set
			if node in openset:
                #Check if we beat the G score 
				new_g = current.G + 1
				if node.G > new_g:
                    #If so, update the node to have a new parent
					node.G = new_g
					node.parent = current
			else:
                #If it isn't in the open set, calculate the G and H score for the node
				node.G = current.G + 1
				node.H = ai.getDistTanks(node.playerTank, goal)
                #Set the parent to our current item
				node.parent = current
                #Add it to the set
				openset.add(node)