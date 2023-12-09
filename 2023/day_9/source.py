from pathlib import WindowsPath

input_path = WindowsPath(__file__).parent / 'input.txt'

def get_next_value(history):
	original_vals = [int(i) for i in history.split()]
	last_vals = [original_vals[-1]]
	depth = 1
	diffs = [original_vals[i] - original_vals[i - 1] for i in range(1, len(original_vals))]
	print(diffs)
	while len(set(diffs) | set([0])) != 1:
		depth += 1
		last_vals.append(diffs[-1])
		diffs = [diffs[i] - diffs[i - 1] for i in range(1, len(diffs))]
	print(sum(last_vals))
	return sum(last_vals)

def part1():
	lines = []
	with open(input_path) as f:
		lines = f.readlines()
	
	return f"Part 1: {sum([get_next_value(line) for line in lines])}"

def get_first_value(history):
	original_vals = [int(i) for i in history.split()]
	first_vals = [original_vals[0]]
	depth = 1
	diffs = [original_vals[i] - original_vals[i - 1] for i in range(1, len(original_vals))]
	while len(set(diffs) | set([0])) != 1:
		depth += 1
		first_vals.append(diffs[0])
		diffs = [diffs[i] - diffs[i - 1] for i in range(1, len(diffs))]
	
	first_vals.reverse()
	result = 0
	for val in first_vals:
		result = val - result
	
	return result

def part2():
	lines = []
	with open(input_path) as f:
		lines = f.readlines()
	
	return f"Part 2: {sum([get_first_value(line) for line in lines])}"

print(part1())
print(part2())
