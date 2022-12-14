from pathlib import WindowsPath
import ast
from functools import cmp_to_key

input_path = WindowsPath(__file__).parent / 'day14.txt'

def render_cave(rock, sand):
	min_x, min_y, max_x, max_y = 1000, 1000, -1, -1
	for tile in rock:
		min_x = min(tile[0], min_x)
		max_x = max(tile[0], max_x)
		min_y = min(tile[1], min_y)
		max_y = max(tile[1], max_y)
	for tile in sand:
		min_x = min(tile[0], min_x)
		max_x = max(tile[0], max_x)
		min_y = min(tile[1], min_y)
		max_y = max(tile[1], max_y)
	
	for y in range(min_y, max_y + 1):
		line = ''
		for x in range(min_x, max_x + 1):
			if (x, y) in rock:
				line += '#'
			elif (x, y) in sand:
				line += 'o'
			else:
				line += ' '
		print(line)
	print('.............')
	print('.............')

def day_part1():
	input = ''
	with open(input_path) as f:
		input = f.readlines()
	rock_tiles = set()
	
	max_y = 0
	
	# generate rock structures
	for line in input:
		for index, rock_corner in enumerate(line.split(' -> ')):
			new_x, new_y = rock_corner.split(',')
			new_x, new_y = int(new_x), int(new_y)
			if index == 0:
				rock_tiles.add((new_x, new_y))
				continue
			old_x, old_y = line.split(' -> ')[index - 1].split(',')
			old_x, old_y = int(old_x), int(old_y)
			
			if new_y > max_y:
				max_y = new_y
			if old_y > max_y:
				max_y = old_y
			
			if new_x != old_x:
				for x in range(min(old_x, new_x), max(old_x, new_x) + 1):
					rock_tiles.add((x, new_y))
			else: # y != old_y
				for y in range(min(old_y, new_y), max(old_y, new_y) + 1):
					rock_tiles.add((new_x, y))
	
	sand_tiles = set()
	
	# simulate sand
	sand_count = 0
	sand_pos = [500, 0]
	while sand_pos[1] < max_y + 5:
		if (sand_pos[0], sand_pos[1] + 1) not in rock_tiles and (sand_pos[0], sand_pos[1] + 1) not in sand_tiles:
			sand_pos[1] += 1
		elif (sand_pos[0] - 1, sand_pos[1] + 1) not in rock_tiles and (sand_pos[0] - 1, sand_pos[1] + 1) not in sand_tiles:
			sand_pos[0] -= 1
			sand_pos[1] += 1
		elif (sand_pos[0] + 1, sand_pos[1] + 1) not in rock_tiles and (sand_pos[0] + 1, sand_pos[1] + 1) not in sand_tiles:
			sand_pos[0] += 1
			sand_pos[1] += 1
		else: # stuck
			sand_tiles.add((sand_pos[0], sand_pos[1]))
			sand_count += 1
			sand_pos = [500, 0]
			
	render_cave(rock_tiles, sand_tiles)
	
	return sand_count
					


def day_part2():
	input = ''
	with open(input_path) as f:
		input = f.readlines()
	rock_tiles = set()

	max_y = 0

	# generate rock structures
	for line in input:
		for index, rock_corner in enumerate(line.split(' -> ')):
			new_x, new_y = rock_corner.split(',')
			new_x, new_y = int(new_x), int(new_y)
			if index == 0:
				rock_tiles.add((new_x, new_y))
				continue
			old_x, old_y = line.split(' -> ')[index - 1].split(',')
			old_x, old_y = int(old_x), int(old_y)

			if new_y > max_y:
				max_y = new_y
			if old_y > max_y:
				max_y = old_y

			if new_x != old_x:
				for x in range(min(old_x, new_x), max(old_x, new_x) + 1):
					rock_tiles.add((x, new_y))
			else:  # y != old_y
				for y in range(min(old_y, new_y), max(old_y, new_y) + 1):
					rock_tiles.add((new_x, y))

	sand_tiles = set()

	# simulate sand
	sand_count = 0
	sand_pos = [500, 0]
	while True:
		if sand_pos[1] == max_y + 1:
			sand_tiles.add((sand_pos[0], sand_pos[1]))
			sand_count += 1
			sand_pos = [500, 0]
		elif (sand_pos[0], sand_pos[1] + 1) not in rock_tiles and (sand_pos[0], sand_pos[1] + 1) not in sand_tiles:
			sand_pos[1] += 1
		elif (sand_pos[0] - 1, sand_pos[1] + 1) not in rock_tiles and (sand_pos[0] - 1, sand_pos[1] + 1) not in sand_tiles:
			sand_pos[0] -= 1
			sand_pos[1] += 1
		elif (sand_pos[0] + 1, sand_pos[1] + 1) not in rock_tiles and (sand_pos[0] + 1, sand_pos[1] + 1) not in sand_tiles:
			sand_pos[0] += 1
			sand_pos[1] += 1
		else:  # stuck
			sand_tiles.add((sand_pos[0], sand_pos[1]))
			if sand_pos == [500, 0]:
				break
			sand_count += 1
			sand_pos = [500, 0]

	render_cave(rock_tiles, sand_tiles)

	return sand_count + 1

print(f"Part 1 answer: {str(day_part1())}")
print(f"Part 2 answer: {str(day_part2())}")
