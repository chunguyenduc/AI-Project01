import algorithm
import math
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection
import matplotlib.path as mplPath
import argparse

def distance(Point1, Point2):
	return math.sqrt((Point1[0]-Point2[0])**2 + (Point1[1]-Point2[1])**2)
	
def onLine(p, Point1, Point2):	#Check on line
	if p[0] <= max(Point1[0], Point2[0]) and p[0] >= min(Point1[0], Point2[0]) and p[1] <= max(Point1[1], Point2[1]) and p[1] >= min(Point1[1], Point2[1]) and distance(p, Point1) + distance(p, Point2) == distance(Point1, Point2):
		 return True

	return False

def draw_path(polygon_list, start, end, length, width, path, title):

	patches = []

	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.set_xlim([0, length])
	ax.set_ylim([0, width])
	
		
	for i in range(len(polygon_list)):
		pgon = plt.Polygon(polygon_list[i], alpha = 0.5)
		patches.append(pgon)
		
	collection = PatchCollection(patches)
	ax.add_collection(collection)
	
	plt.scatter(start[0], start[1])
	plt.text(start[0]+0.5, start[1]+0.5, "Start", fontsize=9)
	plt.scatter(end[0], end[1])
	plt.text(end[0]+0.5, end[1]+0.5, "Goal", fontsize=9)
	plt.title(title)
	
	if path == -1:
		
		ax.set(xlabel = "Can't find path")	
	else:
		x = []
		y = []
		for i in range(len(path)):
			x.append(path[i][0])
			y.append(path[i][1])

		
		plt.plot(x, y)
		total_cost = 'Total cost: ' + str(len(path))
		ax.set(xlabel = total_cost)
	
def get_maze(maze, polygon_list):
	
	#If not walkable, set maze[][] = 1
	for i in range(len(maze)):
		for j in range(len(maze[0])):
			for k in range(len(polygon_list)):
				#Check corner
				if (i, j) in polygon_list[k]:
					maze[i][j] = 1
				else:
					#Check inside
					bbPath = mplPath.Path(polygon_list[k])
					if bbPath.contains_point((i, j)):
						maze[i][j] = 1
					#Check on line
					else:
						for m in range(len(polygon_list[k])):
							point1 = polygon_list[k][m];
							point2 = polygon_list[k][(m+1)%len(polygon_list[k])]
							if onLine((i, j), point1, point2):
								maze[i][j] = 1
	return maze

	
def main():

	parser = argparse.ArgumentParser()
	parser.add_argument('--input', '-i', required = "True", help = "input file")
	parser.add_argument("--task", "-t", required = "True", choices = ["1", "2"], help = "task need to be done")
	
	args = parser.parse_args()
		
	f = open(args.input, "r")

	line = f.readline()
	length, width = map(int, line.split(','))

	maze = []
	for i in range(length):
		maze.append([0] * width)

	line = f.readline()
	startX, startY, endX, endY = map(int, line.split(',')) 
	

	line = f.readline()
	num_polygon = int(line)

	polygon_list = []
	for i in range(num_polygon):
		line = f.readline()
		x = list(map(int, line.split(',')))
		point_list = []
		for i in range(0, len(x), 2):
			pointX = x[i]
			pointY = x[i+1]
			point_list.append((pointX, pointY))
			
		polygon_list.append(point_list)
	
	maze = get_maze(maze, polygon_list)
	
	start = (startX, startY)
	end = (endX, endY)
	
	#Caluculate path
	path = algorithm.ucs(maze, start, end)
	path1 = algorithm.bfs(maze, start, end)
	path2 = algorithm.dfs(maze, start, end)
	path3 = algorithm.astar(maze, start, end)
	
	
	if args.task == "1":
		#Draw UCS path
		draw_path(polygon_list, start, end, length, width, path, "Uinform Cost Search")
		plt.show()
	elif args.task == "2":
		#Draw BFS, DFS, A* path
		draw_path(polygon_list, start, end, length, width, path1, "Breadth First Search")
		draw_path(polygon_list, start, end, length, width, path2, "Depth First Search")
		draw_path(polygon_list, start, end, length, width, path3, "A* Search")
		plt.show()	


main()
