from pathlib import WindowsPath
import re

input_path = WindowsPath(__file__).parent / 'day5.txt'

def day5(part_1):
	lines = []
	with open(input_path) as f:
		lines = f.read()
	stacks_raw, instructions_raw = lines.split('\n\n')
	stacks_raw = stacks_raw.rsplit('\n', 1)[0] # remove final row
	rows = [[row[i] for i in range(len(row)) if i % 4 - 1 == 0] for row in stacks_raw.split('\n')]

	# rotate 2d array, remove empty elements
	stacks = [[row[i] for row in rows if row[i] != ' '] for i in range(len(rows[0]))]
	
	for instruction in instructions_raw.split('\n'):
		if len(instruction) == 0:
			continue
		nums = re.findall(r'\d+', instruction)
		move_instruction = int(nums[0])
		from_instruction = int(nums[1]) - 1
		to_instruction = int(nums[2]) - 1
		
		moving_list = stacks[from_instruction][0:move_instruction]
		if part_1:
			moving_list.reverse()
		stacks[from_instruction] = stacks[from_instruction][move_instruction:]
		stacks[to_instruction] = moving_list + stacks[to_instruction]
	result = ''
	for stack in stacks:
		result += stack[0]
	return result
		
	

print(f"Part 1 answer: {str(day5(True))}")
print(f"Part 2 answer: {str(day5(False))}")
