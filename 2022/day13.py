from pathlib import WindowsPath
import ast
from functools import cmp_to_key

input_path = WindowsPath(__file__).parent / 'day13.txt'

# return -1 if they're disordered, 0 if they match, or 1 if they're ordered
def compare_packets(a, b):
	if isinstance(a, int) and isinstance(b, int):
		if a < b:
			return 1
		elif a > b:
			return -1
		else:
			return 0
	
	if isinstance(a, int):
		a = [a]
	if isinstance(b, int):
		b = [b]
	
	for i in range(max(len(a), len(b))):
		if i >= len(a):
			return 1
		elif i >= len(b):
			return -1
		result = compare_packets(a[i], b[i])
		if result != 0:
			return result
	return 0
		

def day_part1():
	input = ''
	with open(input_path) as f:
		input = f.read()
	right_order_indices = []
	for index, group in enumerate(input.split('\n\n')):
		a, b = group.strip().split('\n')
		a = ast.literal_eval(a.strip())
		b = ast.literal_eval(b.strip())
		if compare_packets(a, b) > 0:
			right_order_indices.append(index + 1)
	return sum(right_order_indices)


def day_part2():
	input = ''
	with open(input_path) as f:
		input = f.readlines()
	packet_list = []
	for packet in input:
		if len(packet.strip()) == 0:
			continue
		packet_list.append(ast.literal_eval(packet.strip()))
	packet_list.append([[2]])
	packet_list.append([[6]])
	
	packet_list = sorted(packet_list, key=cmp_to_key(compare_packets), reverse=True)
	
	decoder_key = 1
	for index, packet in enumerate(packet_list):
		if packet == [[2]] or packet == [[6]]:
			decoder_key *= index + 1
	return decoder_key

print(f"Part 1 answer: {str(day_part1())}")
print(f"Part 2 answer: {str(day_part2())}")
