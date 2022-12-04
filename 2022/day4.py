from pathlib import WindowsPath

input_path = WindowsPath(__file__).parent / 'day4.txt'

def day4_part1():
	lines = []
	with open(input_path) as f:
		lines = f.readlines()
	fully_contain_count = 0
	for line in lines:
		left, right = line.split(',')
		left_range = set(range(int(left.split('-')[0]), int(left.split('-')[1]) + 1))
		right_range = set(range(int(right.split('-')[0]), int(right.split('-')[1]) + 1))
		if left_range & right_range == right_range or left_range & right_range == left_range:
			fully_contain_count += 1
	return fully_contain_count

def day4_part2():
	lines = []
	with open(input_path) as f:
		lines = f.readlines()
	overlap_count = 0
	for line in lines:
		left, right = line.split(',')
		left_range = set(range(int(left.split('-')[0]), int(left.split('-')[1]) + 1))
		right_range = set(
			range(int(right.split('-')[0]), int(right.split('-')[1]) + 1))
		if len(left_range & right_range) > 0:
			overlap_count += 1
	return overlap_count

print(f"Part 1 score: {str(day4_part1())}")
print(f"Part 2 score: {str(day4_part2())}")
