from pathlib import WindowsPath

input_path = WindowsPath(__file__).parent / 'day18.txt'

def parse_input():
	input = ''
	with open(input_path) as f:
		input = f.readlines()
	return set([tuple([int(i) for i in x.split(',')]) for x in input if len(x.strip()) > 0])

def get_sides(cube):
	return set([
		(cube[0] + 1, cube[1], cube[2]),
		(cube[0] - 1, cube[1], cube[2]),
		(cube[0], cube[1] + 1, cube[2]),
		(cube[0], cube[1] - 1, cube[2]),
		(cube[0], cube[1], cube[2] + 1),
		(cube[0], cube[1], cube[2] - 1)
	])
	
def day_part1():
	cubes = parse_input()
	surface_area = 0
	for cube in cubes:
		surface_area += 6 - len(get_sides(cube) & cubes)
	return surface_area

def cube_in_bounds(cube, bounds):
	return cube[0] >= bounds[0] and cube[1] >= bounds[1] and cube[2] >= bounds[2] and cube[0] <= bounds[3] and cube[1] <= bounds[4] and cube[2] <= bounds[5]

def flood_fill(bounds, cubes):
	search_queue = set()
	blacklist = set()
	filled_cubes = set()
	cur_cube = (bounds[0], bounds[1], bounds[2])
	search_queue.add(cur_cube)
	blacklist.add(cur_cube)
	while len(search_queue) > 0:
		cur_cube = search_queue.pop()
		filled_cubes.add(cur_cube)
		for side in get_sides(cur_cube):
			if side not in blacklist and side not in cubes and cube_in_bounds(side, bounds):
				search_queue.add(side)
				blacklist.add(side)
	return filled_cubes

def day_part2():
	cubes = parse_input()
	# min x, y, z, max x, y, z
	bounds = [100, 100, 100, -1, -1, -1]
	for cube in cubes:
		bounds[0] = min(bounds[0], cube[0])
		bounds[1] = min(bounds[1], cube[1])
		bounds[2] = min(bounds[2], cube[2])
		bounds[3] = max(bounds[3], cube[0])
		bounds[4] = max(bounds[4], cube[1])
		bounds[5] = max(bounds[5], cube[2])
	bounds[0] -= 1
	bounds[1] -= 1
	bounds[2] -= 1
	bounds[3] += 1
	bounds[4] += 1
	bounds[5] += 1
	
	exterior_air = flood_fill(bounds, cubes)
	surface_area = 0
	for cube in cubes:
		for side in get_sides(cube):
			if side not in cubes and side in exterior_air:
				surface_area += 1
	return surface_area

print(f"Part 1 answer: {str(day_part1())}")
print(f"Part 2 answer: {str(day_part2())}")
