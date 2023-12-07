import functools
from pathlib import WindowsPath

input_path = WindowsPath(__file__).parent / 'input.txt'

def get_hand_type(hand : str):
	counts = list({i: hand.count(i) for i in hand}.values())
	if 5 in counts:
		return 7
	if 4 in counts:
		return 6
	if 3 in counts and 2 in counts:
		return 5 #full house
	if 3 in counts and 1 in counts:
		return 4
	if 2 in counts and 1 in counts and len(counts) == 3:
		return 3
	if len(counts) == 4:
		return 2
	return 1

def card_compare(item_a, item_b):
	hand_a = item_a[0]
	hand_b = item_b[0]
	
	a_type = get_hand_type(hand_a)
	b_type = get_hand_type(hand_b)
	print(f"Hand {hand_a} is {a_type}, {hand_b} is {b_type}")
	if a_type != b_type:
		return a_type - b_type
	
	# A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2
	replacements = [('A', 'E'), ('K', 'D'), ('Q', 'C'), ('J', 'B'), ('T', 'A')]
	num_hand_a = hand_a
	num_hand_b = hand_b
	for repl in replacements:
		num_hand_a = num_hand_a.replace(repl[0], repl[1])
		num_hand_b = num_hand_b.replace(repl[0], repl[1])
	
	return int(num_hand_a, 16) - int(num_hand_b, 16)
	

def part1():
	input = []
	with open(input_path) as f:
		input = f.readlines()
	
	hands = [(line.split(' ')[0], line.split(' ')[1].replace('\n', '')) for line in input]

	hands.sort(key=functools.cmp_to_key(card_compare))
	score = sum([(i + 1) * int(hand[1]) for i, hand in enumerate(hands)])
	
	return score # input

def get_hand_type_2(hand):
	best_score = 0
	for ch in ['A', 'K', 'D', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2']:
		score = get_hand_type(hand.replace('J', ch))
		if score > best_score:
			best_score = score
	return best_score

def card_compare_2(item_a, item_b):
	hand_a = item_a[0]
	hand_b = item_b[0]
	
	a_type = get_hand_type_2(hand_a)
	b_type = get_hand_type_2(hand_b)
	print(f"Hand {hand_a} is {a_type}, {hand_b} is {b_type}")
	if a_type != b_type:
		return a_type - b_type
	
	# A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2
	replacements = [('A', 'E'), ('K', 'D'), ('Q', 'C'), ('J', '1'), ('T', 'A')]
	num_hand_a = hand_a
	num_hand_b = hand_b
	for repl in replacements:
		num_hand_a = num_hand_a.replace(repl[0], repl[1])
		num_hand_b = num_hand_b.replace(repl[0], repl[1])
	
	return int(num_hand_a, 16) - int(num_hand_b, 16)

def part2():
	input = []
	with open(input_path) as f:
		input = f.readlines()
	
	hands = [(line.split(' ')[0], line.split(' ')[1].replace('\n', '')) for line in input]

	hands.sort(key=functools.cmp_to_key(card_compare_2))
	print(hands)
	score = sum([(i + 1) * int(hand[1]) for i, hand in enumerate(hands)])
	
	return score # input

print(part1())
print(part2())
