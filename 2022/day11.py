from pathlib import WindowsPath
from math import floor

input_path = WindowsPath(__file__).parent / 'day11.txt'

monkeys = []

class Monkey:
	def __init__(self, items, test_num, operation, true_monkey_index, false_monkey_index, worry_divisor):
		self.items = items
		self.test_num = test_num
		self.operation = operation
		self.true_monkey_index = true_monkey_index
		self.false_monkey_index = false_monkey_index
		self.inspect_count = 0
		self.worry_divisor = worry_divisor
	
	def take_turn(self, modulo=1):
		prev_inspect_count = self.inspect_count
		for item in self.items:
			old = item # used in eval
			worry = eval(self.operation)
			
			if self.worry_divisor != 1:
				worry = floor(worry / self.worry_divisor)
			
			if modulo != 1:
				worry %= modulo
			
			if worry % self.test_num == 0:
				monkeys[self.true_monkey_index].items.append(worry)
			else:
				monkeys[self.false_monkey_index].items.append(worry)
			self.inspect_count += 1
		self.items.clear()
		return self.inspect_count - prev_inspect_count

def make_monkeys(input, worry_divisor):
	monkeys.clear()
	monkey_group = input.split('\n\n')
	for monkey_data in monkey_group:
		lines = monkey_data.split('\n')
		items = [int(x.strip()) for x in lines[1].split(':')[1].split(', ')]
		operation = lines[2].split('=')[1].strip()
		test_num = int(lines[3].rsplit(' ', 1)[1])
		true_index = int(lines[4].rsplit(' ', 1)[1])
		false_index = int(lines[5].rsplit(' ', 1)[1])
		m = Monkey(items=items, test_num=test_num, operation=operation, true_monkey_index=true_index, false_monkey_index=false_index, worry_divisor=worry_divisor)
		monkeys.append(m)

def day_part1():
	input = ''
	with open(input_path) as f:
		input = f.read()
	make_monkeys(input, 3)
	
	round_count = 20
	for round in range(round_count):
		for monkey in monkeys:
			monkey.take_turn()
	sorted_monkeys = sorted(monkeys, key=lambda m: m.inspect_count, reverse=True)
	return sorted_monkeys[0].inspect_count * sorted_monkeys[1].inspect_count

def day_part2():
	input = ''
	with open(input_path) as f:
		input = f.read()
	make_monkeys(input, 1)

	round_count = 10000
	
	monkey_modulo = 1
	for monkey in monkeys:
		monkey_modulo *= monkey.test_num
	print(f"monkey modulo {monkey_modulo}")
	
	for round in range(round_count):
		for monkey in monkeys:
			monkey.take_turn(monkey_modulo)
		#print(f"Round {round} complete")
	sorted_monkeys = sorted(monkeys, key=lambda m: m.inspect_count, reverse=True)
	return sorted_monkeys[0].inspect_count * sorted_monkeys[1].inspect_count

print(f"Part 1 answer: {str(day_part1())}")
print(f"Part 2 answer: {str(day_part2())}")
