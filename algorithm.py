import queue
import time


class Node():


	def __init__(self, parent = None, position = None):
		self.parent = parent
		self.position = position

		self.g = 0
		self.h = 0
		self.f = 0

	def __eq__(self, node):
		return self.position == node.position
		
	def __hash__(self):
		return hash(self.position)
	def __lt__(self, other): 
		if(self.f < other.f): 
			return True
		else: 
			return False

def create_child_node(maze, node):

	children = []
	
	for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:

		# Get child node position
		node_position = (node.position[0] + new_position[0], node.position[1] + new_position[1])

		# Make sure within range
		if node_position[0] > (len(maze) - 1) or node_position[0] <= 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] <= 0:
			continue

		# Make sure walkable
		if maze[node_position[0]][node_position[1]] == 1:
			continue

		# Create new node
		new_node = Node(node, node_position)

		# Append
		children.append(new_node)
		
	return children
	
def get_path(node):
	path = []
	current = node
	while current is not None:
		path.append(current.position)
		current = current.parent

	return path[::-1] # Return reversed path	
	
def astar(maze, start, end):

	# Create start and end node
	start_node = Node(None, start)
	start_node.g = start_node.h = start_node.f = 0
	end_node = Node(None, end)
	end_node.g = end_node.h = end_node.f = 0

	# Initialize open and closed list
	open_list = []
	closed_list = set()

	# Add the start node
	open_list.append(start_node)

	# Loop until the end
	while len(open_list) > 0:

		# Get the current node
		current_node = open_list[0]
		current_index = 0
		# Find node with smallest f
		for index, item in enumerate(open_list):
			if item.f < current_node.f:
				current_node = item
				current_index = index

		# Pop current off open list, add to closed list
		
		open_list.pop(current_index)
		closed_list.add(current_node)

		# Found the goal
		if current_node == end_node:
			return get_path(current_node)
		
		#Create children node
		children = create_child_node(maze, current_node)

		# Loop through children
		for child in children:

			#Check if child is in the closed list
			if child in closed_list:
					continue

			# Create the f, g, and h values
			child.g = current_node.g + 1
			child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)	#Euclide
			child.f = child.g + child.h

			# Child is already in the open list
			open_node = Node()
			for open_node in open_list:
				if child == open_node:
					break
				
			if child == open_node:
				if child.g > open_node.g:
					continue
			# Add the child to the open list
			open_list.append(child)
			
			
	#Open list empty but exit loop mean no path
	return -1

def bfs(maze, start, end):
	visited = set()
	
	# Create start and end node
	start_node = Node(None, start)
	start_node.g = 0
	end_node = Node(None, end)
	end_node.g = 0
	
	queue = []
	queue.append(start_node)
	
	visited.add(start_node)
	
	
	while len(queue) > 0:
	
		current_node = queue[0]
		queue.pop(0)
		
		

		
		#If end
		if current_node.position == end:
			return get_path(current_node)
				
		
		#Create children node
		children = create_child_node(maze, current_node)
		
		for child in children:

			#Check if child is visited
			if child not in visited:
				child.g = current_node.g + 1
				visited.add(child)
				queue.append(child)
		
		
	
	return -1



def ucs(maze, start, end):
	
	start_node = Node(None, start)
	start_node.g = start_node.h = start_node.f = 0
	end_node = Node(None, end)
	end_node.g = end_node.h = end_node.f = 0
	
	
	q = []
	visited = set()

	# Add the start node
	q.append(start_node)
	
	# Loop until the end
	while len(q) > 0:
		current_node = q[0]
		
		#Find smallest g node
		min_index = 0
		for i in range(len(q)):
			if q[i].g < current_node.g:
				current_node = q[i]
				min_index = i
			
		visited.add(current_node)
		q.pop(min_index)
		
		

		#if (current_node.g, current_node.position) not in visited:
		#	visited.add((current_node.g, current_node.position))
		
		# Found the goal
		if current_node == end_node:
			
			return get_path(current_node)
			
		

		#Create children node
		children = create_child_node(maze, current_node)

		# Loop through children
		for child in children:
			
			node = Node()
			if child in visited:
				continue
		
			child.g = current_node.g + 1
			
			
			# Child is already in the open list
			for node in q:
				if child == node:
					break
			if child == node:
				if child.g < node.g:
					node = child
				else:
					continue
			else:
				q.append(child)

		
		#time.sleep(0.5)	
	#Open list empty but exit loop mean no path
	
	return -1
	
def dfs(maze, start, end):
	visited = set()
	
	# Create start and end node
	start_node = Node(None, start)
	end_node = Node(None, end)
	
	stack = []
	stack.append(start_node)
	
	#visited.append(start_node)
	
	
	while len(stack) > 0:
		#current_node = q[0]
		#q.pop(0)
		# Get the current node
		current_node = stack[-1]

		# Pop current off open list
		stack.pop(-1)
		
		if current_node not in visited:
			visited.add(current_node)
		#If end
		if current_node.position == end:
			return get_path(current_node)
				
		
		#Create children node
		children = create_child_node(maze, current_node)
		
		for child in children:
			if child not in visited:		
				stack.append(child)		
	
	return -1
	