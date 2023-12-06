from pathlib import WindowsPath

input_path = WindowsPath(__file__).parent / 'input.txt'

def part1():
	input = ''
	with open(input_path) as f:
		input = f.readlines()
	
	times = input[0].split()[1:]
	distances = input[1].split()[1:]
	
	answer = 1
	for i, time in enumerate(times):
		dist = int(distances[i])
		wins = 0
		for j in range(1, int(time) - 1):
			if (int(time) * j) - (j ** 2) > dist:
				wins += 1
		answer *= wins
	
	return answer

def part2():
	input = ''
	with open(input_path) as f:
		input = f.readlines()
	
	time = input[0].split(':')[1].replace(' ', '')
	dist = input[1].split(':')[1].replace(' ', '')
	
	win_start = 0
	win_end = 0
	for j in range(1, int(time) - 1):
		if (int(time) * j) - (j ** 2) > int(dist):
			win_start = j
			break
	for j in range(int(time) - 1, 1, -1):
		if (int(time) * j) - (j ** 2) > int(dist):
			win_end = j
			break
	
	return (win_end - win_start) + 1

print(part1())
print(part2())
