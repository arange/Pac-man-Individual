# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
	"""
	This class outlines the structure of a search problem, but doesn't implement
	any of the methods (in object-oriented terminology: an abstract class).

	You do not need to change anything in this class, ever.
	"""

	def getStartState(self):
		"""
		Returns the start state for the search problem.
		"""
		util.raiseNotDefined()

	def isGoalState(self, state):
		"""
		  state: Search state

		Returns True if and only if the state is a valid goal state.
		"""
		util.raiseNotDefined()

	def getSuccessors(self, state):
		"""
		  state: Search state

		For a given state, this should return a list of triples, (successor,
		action, stepCost), where 'successor' is a successor to the current
		state, 'action' is the action required to get there, and 'stepCost' is
		the incremental cost of expanding to that successor.
		"""
		util.raiseNotDefined()

	def getCostOfActions(self, actions):
		"""
		 actions: A list of actions to take

		This method returns the total cost of a particular sequence of actions.
		The sequence must be composed of legal moves.
		"""
		util.raiseNotDefined()


def tinyMazeSearch(problem):
	"""
	Returns a sequence of moves that solves tinyMaze.  For any other maze, the
	sequence of moves will be incorrect, so only use this for tinyMaze.
	"""
	from game import Directions
	s = Directions.SOUTH
	w = Directions.WEST
	return  [s, s, w, s, w, w, s, w]

def blindSearch(problem,structure):
	"*** YOUR CODE HERE ***"
	
	# example of state: (34, 16)
	# example of successors: [((34, 15), 'South', 1), ((33, 16), 'West', 1)]

	# storage stores all current poissible routes
	storage = structure
	# manually put starting node into storage
	startState = problem.getStartState()
	startNode = (startState,'Stop',0)
	storage.push([startNode])
	# put visited nodes into visited list
	visitedList = []

	while not storage.isEmpty():
		
		# route.append(storage.pop())

		# dequeue the first path in storage, check if it can lead to the goal
		# by 'first path', the data sturcture used doesn't matter, pop() will dequeue the correct path
		route = storage.pop()
		currentNode = route[-1]
		currentState = currentNode[0]
		"*** The successors can not be added here, otherwise the goal state will be expanded ***"
		"*** This is due to the requirement of autograding ***"
		# successors = problem.getSuccessors(currentState)

		# check if current state is the goal state
		if problem.isGoalState(currentState):
			# return the correct route (directions) from 2nd node to goal 
			directions = []
			for node in route:
				directions.append(node[1])
			return directions[1:]
		# check if current node was visited
		if currentState not in visitedList:
			# insert current node into visited list
			visitedList.append(currentState)

			successors = problem.getSuccessors(currentState)
			for successor in successors:
				if successor[0] not in visitedList:
					"*** The whole new 'correct' path is stored instead of just the successor node ***"
					"*** Backtrack is more complicated ***"
					successorPath = route[:]
					successorPath.append(successor)
					storage.push(successorPath)

	return False


def depthFirstSearch(problem):
	"""
	Search the deepest nodes in the search tree first.

	Your search algorithm needs to return a list of actions that reaches the
	goal. Make sure to implement a graph search algorithm.

	To get started, you might want to try some of these simple commands to
	understand the search problem that is being passed in:

	print "Start:", problem.getStartState()
	print "Is the start a goal?", problem.isGoalState(problem.getStartState())
	print "Start's successors:", problem.getSuccessors(problem.getStartState())
	"""
	# Command you should run is:
	# python pacman.py -l mediumMaze -p SearchAgent -a fn=dfs
	"*** YOUR CODE HERE ***"
	structure = util.Stack()

	return blindSearch(problem,structure)

	# util.raiseNotDefined()

def breadthFirstSearch(problem):
	"""Search the shallowest nodes in the search tree first."""
	"*** YOUR CODE HERE ***"
	structure = util.Queue()

	return blindSearch(problem,structure)
	
	# util.raiseNotDefined()

def uniformCostSearch(problem):
	"""Search the node of least total cost first."""
	"*** YOUR CODE HERE ***"

	# storage stores all the possible routes
	storage = util.PriorityQueue()
	# manually put starting node into storage
	startState = problem.getStartState()
	startNode = (startState,'Stop',0)
	# initially the cost of starting point is set to 0
	storage.push([startNode], 0)

	visitedList = []

	while not storage.isEmpty():
		# Dequeue the maximum priority element from the queue
		route = storage.pop()

		currentNode = route[-1]
		currentState = currentNode[0]

		if problem.isGoalState(currentState):
			# return the correct route (directions) from 2nd node to goal 
			directions = []
			for node in route:
				directions.append(node[1])
			return directions[1:]

		# check if current node was visited
		if currentState not in visitedList:
			# insert current node into visited list
			visitedList.append(currentState)

			successors = problem.getSuccessors(currentState)
			for successor in successors:
				if successor[0] not in visitedList:
					successorPath = route[:]
					p_successor = (successor[0], successor[1], successor[2] + currentNode[2])
					newPriority = p_successor[2]
					successorPath.append(p_successor)
					storage.push(successorPath, newPriority)

	return False

def nullHeuristic(state, problem=None):
	"""
	A heuristic function estimates the cost from the current state to the nearest
	goal in the provided SearchProblem.  This heuristic is trivial.
	"""
	return 0

def aStarSearch(problem, heuristic=nullHeuristic):
	"""Search the node that has the lowest combined cost and heuristic first."""
	"*** YOUR CODE HERE ***"
	# storage stores all the possible routes
	storage = util.PriorityQueue()
	# manually put starting node into storage
	startState = problem.getStartState()
	startNode = (startState,'Stop',0)
	# initially the cost of starting point is set to 0
	storage.push([startNode], heuristic(startState, problem))

	visitedList = []

	while not storage.isEmpty():
		# Dequeue the maximum priority element from the queue
		route = storage.pop()

		currentNode = route[-1]
		currentState = currentNode[0]

		if problem.isGoalState(currentState):
			# return the correct route (directions) from 2nd node to goal 
			directions = []
			for node in route:
				directions.append(node[1])
			return directions[1:]

		# check if current node was visited
		if currentState not in visitedList:
			# insert current node into visited list
			visitedList.append(currentState)

			successors = problem.getSuccessors(currentState)
			for successor in successors:
				if successor[0] not in visitedList:
					successorPath = route[:]
					p_successor = (successor[0], successor[1], successor[2] + currentNode[2])
					newPriority = p_successor[2] + heuristic(successor[0], problem)
					successorPath.append(p_successor)
					storage.push(successorPath, newPriority)

	return False


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
