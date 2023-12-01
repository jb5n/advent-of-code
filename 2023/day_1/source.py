from pathlib import WindowsPath
import re

input_path = WindowsPath(__file__).parent / 'input.txt'

def part1():
	lines = []
	with open(input_path) as f:
		lines = f.readlines()
	
	total = 0
	for line in lines:
		line_str = ''.join([i for i in line if i.isdigit()])
		total += int(line_str[0] + line_str[-1])
	
	return str(total)

def part2():
	lines = []
	with open(input_path) as f:
		lines = f.readlines()
	
	numwords = ['---', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
	
	total = 0
	for line in lines:
		earliest_index = 10000000000
		earliest_word = -1
		latest_index = -1
		latest_word = -1
		for i, numword in enumerate(numwords):
			earliest = [i.start() for i in re.finditer(numword, line) if i.start() < earliest_index]
			latest = [i.start() for i in re.finditer(numword, line) if i.start() > latest_index]
			if earliest:
				earliest_index = earliest[0]
				earliest_word = i
			if latest:
				latest_index = latest[-1]
				latest_word = i
		
		earliest_num = [int(ch) for i, ch in enumerate(line) if ch.isdigit() and i < earliest_index]
		earliest_num = earliest_num[0] if earliest_num else earliest_word
		latest_num = [int(ch) for i, ch in enumerate(line) if ch.isdigit() and i > latest_index]
		latest_num = latest_num[-1] if latest_num else latest_word
		total += earliest_num * 10 + latest_num
	return total

print(part1())
print("")
print(part2())
