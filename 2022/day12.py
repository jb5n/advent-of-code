from pathlib import WindowsPath
import astar

input_path = WindowsPath(__file__).parent / 'day12.txt'

def day_part1():
	input = ''
	with open(input_path) as f:
		input = f.read()
	nav_grid = [[ch for ch in line] for line in input.split('\n') if len(line) > 0]
	start_index = (-1,-1)
	end_index = (-1,-1)
	
	width = len(nav_grid)
	height = len(nav_grid[0])
	
	for x in range(width):
		for y in range(height):
			if nav_grid[x][y] == 'S':
				start_index = (x,y)
			elif nav_grid[x][y] == 'E':
				end_index = (x,y)
			if start_index != (-1,-1) and end_index != (-1,-1):
				break
		if start_index != (-1,-1) and end_index != (-1,-1):
			break
	
	if start_index == (-1,-1):
		print("CANNOT FIND START INDEX")
		return 0
	elif end_index == (-1,-1):
		print("CANNOT FIND END INDEX")
		return 0
	
	def heuristic_cost(n, goal):
		return 1
	
	def get_value(n):
		ch = nav_grid[n[0]][n[1]]
		if ch == 'S':
			ch = 'a'
		elif ch == 'E':
			ch = 'z'
		return ord(ch) - ord('a')
	
	def get_neighbors(n):
		cardinal_dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
		neighbors = []
		for dir in cardinal_dirs:
			adjacent = (n[0] + dir[0], n[1] + dir[1])
			if adjacent[0] < 0 or adjacent[0] >= width or adjacent[1] < 0 or adjacent[1] >= height:
				continue
			if get_value(adjacent) - get_value(n) > 1:
				continue
			neighbors.append(adjacent)
		return neighbors
			
	path = list(astar.find_path(start_index, end_index, neighbors_fnct=get_neighbors, heuristic_cost_estimate_fnct=heuristic_cost))
	return len(path) - 1 # remove starting place


def day_part2():
	input = ''
	with open(input_path) as f:
		input = f.read()
	nav_grid = [[ch for ch in line]
             for line in input.split('\n') if len(line) > 0]
	end_index = (-1, -1)
	
	potential_starts = []

	width = len(nav_grid)
	height = len(nav_grid[0])

	for x in range(width):
		for y in range(height):
			if nav_grid[x][y] == 'S' or nav_grid[x][y] == 'a':
				potential_starts.append((x, y))
			elif nav_grid[x][y] == 'E':
				end_index = (x, y)

	if end_index == (-1, -1):
		print("CANNOT FIND END INDEX")
		return 0

	def heuristic_cost(n, goal):
		return 1

	def get_value(n):
		ch = nav_grid[n[0]][n[1]]
		if ch == 'S':
			ch = 'a'
		elif ch == 'E':
			ch = 'z'
		return ord(ch) - ord('a')

	def get_neighbors(n):
		cardinal_dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
		neighbors = []
		for dir in cardinal_dirs:
			adjacent = (n[0] + dir[0], n[1] + dir[1])
			if adjacent[0] < 0 or adjacent[0] >= width or adjacent[1] < 0 or adjacent[1] >= height:
				continue
			if get_value(adjacent) - get_value(n) > 1:
				continue
			neighbors.append(adjacent)
		return neighbors
	
	shortest_path = 1000000
	for start in potential_starts:		
		path = astar.find_path(start, end_index, neighbors_fnct=get_neighbors, heuristic_cost_estimate_fnct=heuristic_cost)
		if path == None:
			continue
		dist = len(list(path)) - 1
		if dist < shortest_path:
			shortest_path = dist
	return shortest_path

print(f"Part 1 answer: {str(day_part1())}")
print(f"Part 2 answer: {str(day_part2())}")
