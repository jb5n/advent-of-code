from pathlib import WindowsPath

input_path = WindowsPath(__file__).parent / 'day8.txt'

def day_part1():
	lines = ''
	with open(input_path) as f:
		lines = f.readlines()
	all_trees = [[ch for ch in line.strip()] for line in lines]
	all_trees_rot = list(zip(*all_trees.copy()))
	valid_trees = []
	for row in range(len(all_trees)):
		for column in range(len(all_trees[row])):
			if row == 0 or row == len(all_trees) - 1 or column == 0 or column == len(all_trees) - 1:
				valid_trees.append(all_trees[row][column])
				continue
			
			tree_height = all_trees[row][column]
			
			left = all_trees[row][:column]
			right = all_trees[row][:column:-1][::-1]
			down = all_trees_rot[column][:row]
			up = all_trees_rot[column][:row:-1][::-1]
			
			if len([x for x in left if x >= tree_height]) == 0 or len([x for x in right if x >= tree_height]) == 0 or \
				len([x for x in down if x >= tree_height]) == 0 or len([x for x in up if x >= tree_height]) == 0:
				valid_trees.append(all_trees[row][column])
	return len(valid_trees)

def day_part2():
	lines = ''
	with open(input_path) as f:
		lines = f.readlines()
	all_trees = [[ch for ch in line.strip()] for line in lines]
	all_trees_rot = list(zip(*all_trees.copy()))
	max_score = 0
	for row in range(len(all_trees)):
		for column in range(len(all_trees[row])):
			tree_height = all_trees[row][column]

			left = all_trees[row][:column]
			right = all_trees[row][:column:-1][::-1]
			down = all_trees_rot[column][:row]
			up = all_trees_rot[column][:row:-1][::-1]
			
			total_score = 1
			for line in [left[::-1], right, down[::-1], up]:
				cur_score = 0
				for x in line:
					cur_score += 1
					if x >= tree_height:
						break
				total_score *= cur_score
			max_score = max(total_score, max_score)
	return max_score
			

print(f"Part 1 answer: {str(day_part1())}")
print(f"Part 2 answer: {str(day_part2())}")
