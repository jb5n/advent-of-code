from pathlib import WindowsPath
from math import lcm

input_path = WindowsPath(__file__).parent / 'input.txt'

def part1():
	lines = []
	with open(input_path) as f:
		lines = f.readlines()
	
	instructions = lines[0]
	desert_map = {line.split(' = ')[0]: (line.split(', ')[0][-3:], line.split(', ')[1][:3]) for line in lines[2:]}
	
	step_count = 0
	cur_loc = 'AAA'
	while cur_loc != 'ZZZ':
		dir_index = step_count % (len(lines[0]) - 1)
		turn_dir = 0 if instructions[dir_index] == 'L' else 1
		cur_loc = desert_map[cur_loc][turn_dir]
		step_count += 1
	
	return step_count

def part2():
	lines = []
	with open(input_path) as f:
		lines = f.readlines()
	
	instructions = lines[0]
	desert_map = {line.split(' = ')[0]: (line.split(', ')[0][-3:], line.split(', ')[1][:3]) for line in lines[2:]}
	
	locs = [loc for loc in desert_map.keys() if 'A' in loc]
	
	z_occurrences = {}
	for i in range(len(locs)):
		z_occurrence = []
		step_count = 0
		original_loc = locs[i]
		for j in range(100000):
			dir_index = step_count % (len(lines[0]) - 1)
			turn_dir = 0 if instructions[dir_index] == 'L' else 1
			locs[i] = desert_map[locs[i]][turn_dir]
			if 'Z' in locs[i]:
				z_occurrence.append(j + 1)
			step_count += 1
		z_occurrences[original_loc] = z_occurrence
	
	bases = [occurence[0] for occurence in z_occurrences.values()]
	total_lcm = 1
	for base in bases:
		total_lcm = lcm(base, total_lcm)

	return total_lcm

print(part1())
print(part2())
