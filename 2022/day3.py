from pathlib import WindowsPath

input_path = WindowsPath(__file__).parent / 'day3.txt'

def calc_score(character : str):
	if character.isupper():
		return ord(character) - ord('A') + 27
	else:
		return ord(character) - ord('a') + 1

def day3_part1():
	lines = []
	with open(input_path) as f:
		lines = f.readlines()
	score = 0
	for line in lines:
		left, right = line[:len(line) // 2], line[len(line) // 2:]
		match = [x for x in left if x in right]
		score += calc_score(match[0])
	return score

def day3_part2():
	lines = []
	with open(input_path) as f:
		lines = f.readlines()
	score = 0
	for i in range(0, len(lines), 3):
		a, b, c = lines[i], lines[i + 1], lines[i + 2]
		badge = [x for x in a if x in b and x in c]
		score += calc_score(badge[0])
	return score

print(f"Part 1 score: {str(day3_part1())}")
print(f"Part 2 score: {str(day3_part2())}")
