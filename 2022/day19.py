from pathlib import WindowsPath
import re
import treelib
import math

input_path = WindowsPath(__file__).parent / 'day19.txt'

resource_names = ['ore', 'clay', 'obsidian', 'geode']
current_maximum_geodes = -1

def parse_input():
	input = ''
	with open(input_path) as f:
		input = f.readlines()
	blueprints = []
	for line in input:
		if line.strip() == '':
			continue
		
		nums = [int(s) for s in re.findall(r'-?\d+\.?\d*', line)]
		blueprints.append({
			'id': nums[0],
			'ore': {'ore': nums[1]},
			'clay': {'ore': nums[2]},
			'obsidian': {'ore': nums[3], 'clay': nums[4]},
			'geode': {'ore': nums[5], 'obsidian': nums[6]}
		})
	return blueprints

def construct_robot(blueprint : dict, robot_type : str, robots_owned : dict, resources : dict, minutes_left : int):
	global current_maximum_geodes
	
	construction_time = 0
	for resource, res_count in blueprint[robot_type].items():
		if robots_owned[resource] == 0:
			return -1 # can't ever produce this robot yet because we don't produce the resources needed for it
		construction_time = max(construction_time, math.ceil(res_count / robots_owned[resource]))
	
	print(minutes_left)
	
	minutes_left -= construction_time
	if minutes_left <= 0: # time's up
		if resources['geode'] > current_maximum_geodes:
			current_maximum_geodes = resources['geode']
		return resources['geode']
	
	# robot resource gathering
	for resource, res_count in robots_owned.items():
		resources[resource] += res_count * construction_time
	
	# robot construction takes away these resources
	for resource, res_count in blueprint[robot_type].items():
		resources[resource] -= res_count
	robots_owned[robot_type] += 1
	
	if resources['geode'] + minutes_left < current_maximum_geodes:
		return resources['geode']
	
	max_geodes = -1
	for next_robot_type in resource_names:
		max_geodes = max(max_geodes, construct_robot(blueprint, next_robot_type, robots_owned.copy(), resources.copy(), minutes_left))
	if max_geodes > current_maximum_geodes:
		current_maximum_geodes = max_geodes
	return max_geodes

def evaluate_blueprint(blueprint):
	global current_maximum_geodes
	
	robots = { 'ore': 1, 'clay': 0, 'obsidian': 0, 'geode': 0 }
	resources = { 'ore': 0, 'clay': 0, 'obsidian': 0, 'geode': 0 }
	minutes_left = 24
	max_geodes = -1
	for next_robot_type in resource_names:
		max_geodes = max(max_geodes, construct_robot(blueprint, next_robot_type, robots, resources, minutes_left))
		if max_geodes > current_maximum_geodes:
			current_maximum_geodes = max_geodes
	return max_geodes

def day_part1():
	blueprints = parse_input()
	all_quality = 0
	for bp in blueprints:
		all_quality += evaluate_blueprint(bp) * bp['id']
	return all_quality
	

def day_part2():
	cubes = parse_input()


print(f"Part 1 answer: {str(day_part1())}")
print(f"Part 2 answer: {str(day_part2())}")
