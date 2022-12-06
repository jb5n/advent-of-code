from pathlib import WindowsPath

input_path = WindowsPath(__file__).parent / 'day6.txt'

def day6(marker_length):
	input = ''
	with open(input_path) as f:
		input = f.read()
	for i in range(marker_length, len(input)):
		if len(set(input[i - marker_length:i])) == len(list(input[i - marker_length:i])):
			return i
	return "FAILED TO FIND OUTPUT"

print(f"Part 1 answer: {str(day6(4))}")
print(f"Part 2 answer: {str(day6(14))}")
