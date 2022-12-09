from pathlib import WindowsPath

input_path = WindowsPath(__file__).parent / 'day9.txt'

def day_part1():
	lines = ''
	with open(input_path) as f:
		lines = f.readlines()
	head_pos = dict(x=0, y=0)
	tail_pos = dict(x=0, y=0)
	visited = [[0,0]]
	for line in lines:
		dir, count = line.split(' ')
		for _ in range(int(count)):
			if dir == 'R':
				head_pos['x'] += 1
			elif dir == 'L':
				head_pos['x'] -= 1
			elif dir == 'U':
				head_pos['y'] += 1
			elif dir == 'D':
				head_pos['y'] -= 1
			else:
				print("INVALID DIRECTION " + dir)
			
			if abs(head_pos['x'] - tail_pos['x']) < 2 and abs(head_pos['y'] - tail_pos['y']) < 2:
				continue
			
			# move orthogonally
			if dir == 'R':
				tail_pos['x'] += 1
			elif dir == 'L':
				tail_pos['x'] -= 1
			elif dir == 'U':
				tail_pos['y'] += 1
			elif dir == 'D':
				tail_pos['y'] -= 1
			
			# move diagonally
			if (dir == 'R' or dir == 'L') and tail_pos['y'] != head_pos['y']:
				tail_pos['y'] = head_pos['y']
			elif (dir == 'U' or dir == 'D') and tail_pos['x'] != head_pos['x']:
				tail_pos['x'] = head_pos['x']
			visited.append([tail_pos['x'], tail_pos['y']])
	visited_set = []
	[visited_set.append(x) for x in visited if x not in visited_set]
	return len(visited_set)

def day_part2():
	lines = ''
	with open(input_path) as f:
		lines = f.readlines()
	knots = []
	for _ in range(10):
		knots.append(dict(x=0, y=0))
	visited = [[0, 0]]
	for line in lines:
		dir, count = line.split(' ')
		for i in range(int(count)):
			if dir == 'R':
				knots[0]['x'] += 1
			elif dir == 'L':
				knots[0]['x'] -= 1
			elif dir == 'U':
				knots[0]['y'] += 1
			elif dir == 'D':
				knots[0]['y'] -= 1
			else:
				print("INVALID DIRECTION " + dir)
			
			for k in range(1, len(knots)):
				if abs(knots[k - 1]['x'] - knots[k]['x']) < 2 and abs(knots[k - 1]['y'] - knots[k]['y']) < 2:
					break

				if knots[k - 1]['x'] > knots[k]['x']:
					knots[k]['x'] += 1
				elif knots[k - 1]['x'] < knots[k]['x']:
					knots[k]['x'] -= 1
				if knots[k - 1]['y'] > knots[k]['y']:
					knots[k]['y'] += 1
				elif knots[k - 1]['y'] < knots[k]['y']:
					knots[k]['y'] -= 1
			visited.append([knots[9]['x'], knots[9]['y']])
	visited_set = []
	[visited_set.append(x) for x in visited if x not in visited_set]
	return len(visited_set)
			

print(f"Part 1 answer: {str(day_part1())}")
print(f"Part 2 answer: {str(day_part2())}")
