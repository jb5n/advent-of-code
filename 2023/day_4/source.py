from pathlib import WindowsPath
import math

input_path = WindowsPath(__file__).parent / 'input.txt'

def part1():
	lines = []
	with open(input_path) as f:
		lines = f.readlines()
		
	return sum([math.floor(2 ** (len(set(filter(None, line.replace('\n', '').split(':')[1].split('|')[0].split(' '))) & set(filter(None, line.replace('\n', '').split(':')[1].split('|')[1].split(' ')))) - 1)) for line in lines])

def part2():
	lines = []
	with open(input_path) as f:
		lines = f.readlines()
	
	card_wins = []
	
	def score_card(card_index):
		if len(card_wins[card_index]) == 0:
			return 1
		else:
			return sum([score_card(i) for i in card_wins[card_index]]) + 1
	
	for i, line in enumerate(lines):
		win_count = len(set(filter(None, line.replace('\n', '').split(':')[1].split('|')[0].split(' '))) & set(filter(None, line.replace('\n', '').split(':')[1].split('|')[1].split(' '))))
		card_wins.append(list(range(i + 1, i + win_count + 1)))
	
	wins_total = 0
	for i in range(len(lines)):
		wins_total += score_card(i)
	return wins_total

print(part1())
print(part2())
