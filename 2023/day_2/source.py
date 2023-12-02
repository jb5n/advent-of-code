from pathlib import WindowsPath

input_path = WindowsPath(__file__).parent / 'input.txt'

def is_valid_draw(cube_desc):
	num = ''.join([i for i in cube_desc if i.isdigit()])
	colors = 'dgb'
	max_cubes_by_color = [12, 13, 14]
	index = colors.index(list(set(cube_desc) & set(colors))[0])
	return int(num) <= max_cubes_by_color[index]

def part1():
	lines = []
	with open(input_path) as f:
		lines = [ln.split(':')[1] for ln in f.readlines()]
	
	valid_games = []
	for i, ln in enumerate(lines):
		valid_cube_draws = [draw for draw in ln.split(';') if len([cube for cube in draw.split(',') if is_valid_draw(cube)]) == len(draw.split(','))]
		if len(valid_cube_draws) == len(ln.split(';')):
			valid_games.append(i + 1)
			print(f"{i + 1} is valid!")
	
	return sum(valid_games)

# returns (num, color_index)
def get_reqd_colors(cube_desc):
	num = ''.join([i for i in cube_desc if i.isdigit()])
	colors = 'dgb'
	index = colors.index(list(set(cube_desc) & set(colors))[0])
	return int(num), index

def part2():
	lines = []
	with open(input_path) as f:
		lines = [ln.split(':')[1] for ln in f.readlines()]
	
	total = 0
	for ln in lines:
		max_colors = [0, 0, 0]
		for draw in ln.split(';'):
			for cube in draw.split(','):
				num, color_index = get_reqd_colors(cube)
				max_colors[color_index] = max(max_colors[color_index], num)
		total += max_colors[0] * max_colors[1] * max_colors[2]
		print(f"Required: {max_colors[0]} red {max_colors[1]} green {max_colors[2]} blue")
	
	return total

print(part1())
print(part2())
