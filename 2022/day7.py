from pathlib import WindowsPath
from anytree import AnyNode, RenderTree, PreOrderIter, search

input_path = WindowsPath(__file__).parent / 'day7.txt'

def day7_part1():
	input = ''
	with open(input_path) as f:
		input = f.read()
	input = input.split('\n', 1)[1]  # skip the first cd /
	root = AnyNode(id='/', size=0)
	working_dir = root
	for cmd in input.split('$ '):
		print(cmd.strip())
		if cmd.startswith('cd'):
			if '..' in cmd:
				working_dir = working_dir.parent
			else:
				working_dir = search.find(working_dir, lambda node: node.id == cmd.replace(
					'cd ', '').strip() and node.size == 0 and node.parent == working_dir)
		elif cmd.startswith('ls'):
			for content in cmd.split('\n')[1:]: # skip the first line with ls
				if len(content) == 0:
					continue
				left, right = content.strip().split(' ')
				size = 0
				if left != 'dir':
					size = int(left)
				AnyNode(id=right, parent=working_dir, size=size)
		else:
			print(f"INVALID COMMAND {cmd}")
	print(RenderTree(root))
	
	dirs_by_size = {}
	for node in PreOrderIter(root):
		if node.size == 0:
			dirs_by_size[node] = sum([child.size for child in PreOrderIter(node)])
	return sum([dirs_by_size[x] for x in dirs_by_size if dirs_by_size[x] <= 100000])

def day7_part2():
	input = ''
	with open(input_path) as f:
		input = f.read()
	input = input.split('\n', 1)[1]  # skip the first cd /
	root = AnyNode(id='/', size=0)
	working_dir = root
	for cmd in input.split('$ '):
		print(cmd.strip())
		if cmd.startswith('cd'):
			if '..' in cmd:
				working_dir = working_dir.parent
			else:
				working_dir = search.find(working_dir, lambda node: node.id == cmd.replace(
					'cd ', '').strip() and node.size == 0 and node.parent == working_dir)
		elif cmd.startswith('ls'):
			for content in cmd.split('\n')[1:]:  # skip the first line with ls
				if len(content) == 0:
					continue
				left, right = content.strip().split(' ')
				size = 0
				if left != 'dir':
					size = int(left)
				AnyNode(id=right, parent=working_dir, size=size)
		else:
			print(f"INVALID COMMAND {cmd}")
	print(RenderTree(root))

	dirs_by_size = {}
	for node in PreOrderIter(root):
		if node.size == 0:
			dirs_by_size[node] = sum([child.size for child in PreOrderIter(node)])
	cur_free_space = 70000000 - dirs_by_size[root]
	delete_size = 30000000 - cur_free_space
	dirs_by_size = dict(sorted(dirs_by_size.items(), key=lambda item: item[1]))
	for dir in dirs_by_size:
		if dirs_by_size[dir] >= delete_size:
			return dirs_by_size[dir]
	return "FAILED"

print(f"Part 1 answer: {str(day7_part1())}")
print(f"Part 2 answer: {str(day7_part2())}")
