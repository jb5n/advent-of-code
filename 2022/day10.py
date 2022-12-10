from pathlib import WindowsPath

input_path = WindowsPath(__file__).parent / 'day10.txt'

def eval_signal(cycle, register_x):
	eval_cycles = [20, 60, 100, 140, 180, 220]
	if cycle not in eval_cycles:
		return 0
	return cycle * register_x

def day_part1():
	lines = ''
	with open(input_path) as f:
		lines = f.readlines()
	cycle = 1
	register_x = 1
	signal_sum = 0
	for line in lines:
		if len(line) == 0:
			continue
		
		if line.strip() == 'noop':
			cycle += 1
			signal_sum += eval_signal(cycle, register_x)
		else:
			cycle += 1
			signal_sum += eval_signal(cycle, register_x)
			cycle += 1
			register_x += int(line.split(' ')[1].strip())
			signal_sum += eval_signal(cycle, register_x)
	return signal_sum

def draw_pixel(cycle, register_positions):
	suffix = ''
	if cycle % 40 == 0:
		suffix = '\n'
	cycle = cycle % 40
	
	if cycle in register_positions or cycle - 1 in register_positions or cycle -2 in register_positions:
		return '#' + suffix
	return '.' + suffix

def day_part2():
	lines = ''
	with open(input_path) as f:
		lines = f.readlines()
	cycle = 1
	register_x = 1
	register_positions = [register_x]
	
	crt_output = '#'
	
	for line in lines:
		if len(line) == 0:
			continue

		if line.strip() == 'noop':
			cycle += 1
			crt_output += draw_pixel(cycle, register_positions)
		else:
			cycle += 1
			crt_output += draw_pixel(cycle, register_positions)
			cycle += 1
			register_x += int(line.split(' ')[1].strip())
			register_positions.clear()
			register_positions.append(register_x)
			crt_output += draw_pixel(cycle, register_positions)
	print(crt_output)
	return 0
			

print(f"Part 1 answer: {str(day_part1())}")
print(f"Part 2 answer: {str(day_part2())}")
