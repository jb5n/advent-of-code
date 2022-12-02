from pathlib import WindowsPath

input_path = WindowsPath(__file__).parent / 'day2.txt'

def calculate_score_1():
	total_score = 0
	with open(input_path) as f:
		for line in f.readlines():
			their_score = ord(line.split(' ')[0]) - ord('A') + 1
			our_score = ord(line.split(' ')[1][0]) - ord('X') + 1
			round_score = our_score
			if their_score == our_score:
				round_score += 3
			elif their_score % 3 == (our_score - 1):
				round_score += 6
			total_score += round_score
	return total_score

def calculate_score_2():
	total_score = 0
	with open(input_path) as f:
		lines = f.readlines()
		for line in lines:
			their_score = ord(line.split(' ')[0]) - ord('A') + 1
			desired_outcome = ord(line.split(' ')[1][0]) - ord('X') + 1
			if desired_outcome == 1: # lose
				round_score = (their_score - 2) % 3 + 1
			elif desired_outcome == 2: # tie
				round_score = their_score + 3
			else: # win
				round_score = (their_score % 3 + 1) + 6
			total_score += round_score
	return total_score

print(f"Part 1 score: {str(calculate_score_1())}")
print(f"Part 2 score: {str(calculate_score_2())}")
