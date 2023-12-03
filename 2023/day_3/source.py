from pathlib import WindowsPath

input_path = WindowsPath(__file__).parent / 'input.txt'

def iterate_2d(input_list):
	for y, row in enumerate(input_list):
		for x, element in enumerate(row):
			yield (x, y, element)

def get_adjacent_to(x, y):
	directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
	return [(x + dir[0], y + dir[1]) for dir in directions]

def part1():
	lines = [] # 2d list [y, x]
	with open(input_path) as f:
		lines = [i for i in f.readlines()]
	
	adjacent_to_symbols = []
	for x, y, element in iterate_2d(lines):
		if not element.isdigit() and element not in ['.', '\n']:
			#print(f"Symbol at {x}, {y}: {element}")
			adjacent_to_symbols.extend(get_adjacent_to(x, y))
	
	total = 0
	for y, row in enumerate(lines):
		num_starts_and_ends = []
		for i, val in enumerate(row):
			if val.isdigit() and (i == 0 or i == len(row) - 1 or not row[i - 1].isdigit() or not row[i + 1].isdigit()):
				num_starts_and_ends.append(i)
				if (i == 0 or not row[i - 1].isdigit()) and (i == len(row) - 1 or not row[i + 1].isdigit()):
					num_starts_and_ends.append(i)
		if len(num_starts_and_ends) == 0:
			continue
		num_starts = num_starts_and_ends[::2]
		#print(f"starts: {num_starts}")
		num_ends = num_starts_and_ends[1::2]
		#print(f"ends: {num_ends}")
		for i, num_start in enumerate(num_starts):
			#print(row[num_start:num_ends[i] + 1])
			for num_end_i in range(num_start, num_ends[i] + 1):
				if (num_end_i, y) in adjacent_to_symbols:
					#print(f"overlap {num_end_i}, {y}")
					total += int(row[num_start:num_ends[i] + 1])
					#print(row[num_start:num_ends[i] + 1])
					break
	
	return total

def part2():
	lines = [] # 2d list [y, x]
	with open(input_path) as f:
		lines = [i for i in f.readlines()]
	
	adjacent_to_gears = {}
	for x, y, element in iterate_2d(lines):
		if element == '*':
			adjacent_to_gears.update({dir: (x, y) for dir in get_adjacent_to(x, y)})
	#print(adjacent_to_gears)
	
	gear_map = {}
	total = 0
	for y, row in enumerate(lines):
		num_starts_and_ends = []
		for i, val in enumerate(row):
			if val.isdigit() and (i == 0 or i == len(row) - 1 or not row[i - 1].isdigit() or not row[i + 1].isdigit()):
				num_starts_and_ends.append(i)
				if (i == 0 or not row[i - 1].isdigit()) and (i == len(row) - 1 or not row[i + 1].isdigit()):
					num_starts_and_ends.append(i)
		if len(num_starts_and_ends) == 0:
			continue
		num_starts = num_starts_and_ends[::2]
		num_ends = num_starts_and_ends[1::2]
		for i, num_start in enumerate(num_starts):
			for num_end_i in range(num_start, num_ends[i] + 1):
				if (num_end_i, y) in adjacent_to_gears:
					gear = adjacent_to_gears[(num_end_i, y)]
					if gear not in gear_map:
						gear_map[gear] = []
					gear_map[gear].append(int(row[num_start:num_ends[i] + 1]))
					break
	
	return sum([val[0] * val[1] for val in list(gear_map.values()) if len(val) == 2])

print(part1())
print(part2())
