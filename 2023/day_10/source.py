from pathlib import WindowsPath

input_path = WindowsPath(__file__).parent / 'input.txt'

def part1():
	lines = []
	with open(input_path) as f:
		lines = f.readlines()
	lines = [line.replace('\n', '') for line in lines]
	
	print(lines)
	
	start_index = ()
	for i, line in enumerate(lines):
		if 'S' in line:
			start_index = (line.index('S'), i)
			break
	
	print(f"start index: {start_index}")
	
	pipe_connections = {
		'|': ((0, 1), (0, -1)),
		'-': ((1, 0), (-1, 0)),
		'L': ((0, -1), (1, 0)),
		'J': ((0, -1), (-1, 0)),
		'7': ((0, 1), (-1, 0)),
		'F': ((0, 1), (1, 0)),
		'.': (),
		'S': ()
	}
	
	def add_points(a, b):
		return (a[0] + b[0], a[1] + b[1])
	
	def sub_points(a, b):
		return (a[0] - b[0], a[1] - b[1])
	
	def connects_to(our_point, eval_point):
		if our_point[1] < 0 or our_point[0] < 0 or our_point[1] >= len(lines) or our_point[0] >= len(lines[our_point[1]]):
			return False
		print(f"Eval {our_point} to {eval_point}, {sub_points(eval_point, our_point)}")
		return sub_points(eval_point, our_point) in pipe_connections[lines[our_point[1]][our_point[0]]]
	
	def step_pipe(cur_pos, last_pos, index):
		for possible_dir in pipe_connections[lines[cur_pos[1]][cur_pos[0]]]:
			new_pos = add_points(cur_pos, possible_dir)
			if new_pos != last_pos and lines[new_pos[1]][new_pos[0]] != 'S':
				print(f"{new_pos}, last is {last_pos}: {lines[new_pos[1]][new_pos[0]]}. Index {index}")
				return new_pos, cur_pos
		return (0, 0), (0, 0)
	
	connected_points = []
	for in_dir in ((start_index[0], start_index[1] + 1), (start_index[0], start_index[1] - 1), (start_index[0] + 1, start_index[1]), (start_index[0] - 1, start_index[1])):
		if connects_to(in_dir, start_index):
			connected_points.append(in_dir)
	
	if len(connected_points) != 2:
		return f"Connected points too many, we have {connected_points}"

	print(f"Connects to {connected_points}")
	
	old_points = [connected_points[0], connected_points[1]]
	steps = 1
	while True:
		connected_points[0], old_points[0] = step_pipe(connected_points[0], old_points[0], 0)
		connected_points[1], old_points[1] = step_pipe(connected_points[1], old_points[1], 1)
		steps += 1
		if connected_points[0] == connected_points[1]:
			print(f"linked on {connected_points[0]}")
			break
		if steps >= len(lines) * len(lines[0]):
			print("Too many steps!")
			break
	
	return f"Required {steps} steps"

def part2():
	lines = []
	with open(input_path) as f:
		lines = f.readlines()
	lines = [line.replace('\n', '') for line in lines]
	
	exploded_characters = {
		'|': ['.x.', '.x.', '.x.'],
		'-': ['...', 'xxx', '...'],
		'L': ['.x.', '.xx', '...'],
		'J': ['.x.', 'xx.', '...'],
		'7': ['...', 'xx.', '.x.'],
		'F': ['...', '.xx', '.x.'],
		'.': ['...', '...', '...'],
		'S': ['...', '...', '...']
	}
	
	def floodfill(matrix, x, y):
		#"hidden" stop clause - not reinvoking for "c" or "b", only for "a".
		if matrix[y][x] == ".":  
			matrix[x][y] = "o"
			#recursively invoke flood fill on all surrounding cells:
			if x > 0:
				floodfill(matrix,x-1,y)
			if x < len(matrix[y]) - 1:
				floodfill(matrix,x+1,y)
			if y > 0:
				floodfill(matrix,x,y-1)
			if y < len(matrix) - 1:
				floodfill(matrix,x,y+1)
	
	exploded_lines = []
	for line in lines:
		exploded_lines.append(''.join([exploded_characters[ch][0] for ch in line]))
		exploded_lines.append(''.join([exploded_characters[ch][1] for ch in line]))
		exploded_lines.append(''.join([exploded_characters[ch][2] for ch in line]))
	print(exploded_lines)
	return ''
	

#print(part1())
print(part2())
