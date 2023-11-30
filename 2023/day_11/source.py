from pathlib import WindowsPath

input_path = WindowsPath(__file__).parent / 'input.txt'

def part1():
	input = ''
	with open(input_path) as f:
		input = f.read()
	return input

def part2():
	input = ''
	with open(input_path) as f:
		input = f.read()
	return input

print(part1())
print(part2())
