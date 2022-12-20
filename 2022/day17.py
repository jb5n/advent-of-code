from pathlib import WindowsPath
from copy import deepcopy

input_path = WindowsPath(__file__).parent / 'day17.txt'

def can_fit(world : set, rock : set, y_origin : int):
	walls = set()
	for i in range(0, 5):
		walls.add((-1, y_origin + i))
		walls.add((7, y_origin + i))
	
	return len(world & rock) == 0 and len(rock & walls) == 0

class RockShape:
	def __init__(self, shapes : set, origin):
		self.shapes = shapes
		self.origin = origin
	
	def shift(self, right : bool):
		self.origin = (self.origin[0] + (1 if right else -1), self.origin[1])
	
	def fall(self):
		self.origin = (self.origin[0], self.origin[1] - 1)
	
	def get_world_set(self, offset):
		world_set = set()
		for shape in self.shapes:
			world_set.add((shape[0] + self.origin[0] + offset[0], shape[1] + self.origin[1] + offset[1]))
		return world_set

def parse_input():
	input = ''
	with open(input_path) as f:
		input = f.read()
	return list(input.strip())

def render_rocks(world, max_y):
	for y in range(max_y, -1, -1):
		line = ''
		for x in range(0, 7):
			if (x, y) in world:
				line += '#'
			else:
				line += ' '
		print(line)

def prune_world(world, min_y):
	return set([x for x in world if x[1] >= min_y])

def day_part1():
	jets = parse_input()
	shape_pool = [
		set([(0, 0), (1, 0), (2, 0), (3, 0)]),
		set([(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)]),
		set([(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]),
		set([(0, 0), (0, 1), (0, 2), (0, 3)]),
		set([(0, 0), (1, 0), (0, 1), (1, 1)])
	]
	
	world = set([(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)])
	max_y = 0
	heightmap = [0, 0, 0, 0, 0, 0, 0]
	
	jet_index = 0
	for rock_count in range(0, 2022):
		rock = RockShape(shape_pool[rock_count % len(shape_pool)], (2, max_y + 4))
		while True:
			shift_right = jets[jet_index % len(jets)] == '>'
			jet_index += 1
			if can_fit(world, rock.get_world_set((1 if shift_right else -1, 0)), rock.origin[1]):
				rock.shift(shift_right)
			if can_fit(world, rock.get_world_set((0, -1)), rock.origin[1]):
				rock.fall()
			else:
				break
		for rock_pos in rock.get_world_set((0, 0)):
			max_y = max(rock_pos[1], max_y)
			heightmap[rock_pos[0]] = max(heightmap[rock_pos[0]], rock_pos[1])
		world = world.union(rock.get_world_set((0, 0)))
		world = prune_world(world, min(heightmap))
	return max_y

print(f"Part 1 answer: {str(day_part1())}")
