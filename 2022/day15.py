from pathlib import WindowsPath
import re

input_path = WindowsPath(__file__).parent / 'day15.txt'

def manhattan_distance(pos1, pos2):
	return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def parse_input():
	input = ''
	with open(input_path) as f:
		input = f.readlines()
	
	sensors = set()
	beacons = set()
	
	for line in input:
		nums = [int(s) for s in re.findall(r'-?\d+\.?\d*', line)]
		
		dist = manhattan_distance(([nums[0], nums[1]]), ([nums[2], nums[3]]))
		
		sensors.add((nums[0], nums[1], dist))
		beacons.add((nums[2], nums[3]))
	return sensors, beacons

def point_in_range(sensor, point):
	return manhattan_distance((sensor[0], sensor[1]), point) <= sensor[2]

def day_part1():
	sensors, beacons = parse_input()
	min_x = 100000
	max_x = -100000
	for sensor in sensors:
		min_x = min(min_x, sensor[0] - sensor[2])
		max_x = max(max_x, sensor[0] + sensor[2])
	
	search_y = 2000000
	invalid_beacon_count = 0
	for x in range(min_x, max_x + 1):
		valid_spot = True
		if (x, search_y) in beacons:
			continue
		
		for sensor in sensors:
			if point_in_range(sensor, (x, search_y)):
				valid_spot = False
				break
		if not valid_spot:
			invalid_beacon_count += 1
	return invalid_beacon_count
	

def get_intersecting_sensors(a, sensors):
	intersecting = set()
	for b in sensors:
		if a == b:
			continue
		if manhattan_distance(a, b) < a[2] + b[2]:
			intersecting.add(b)
	return intersecting
	
def in_bounds(pt, min_pt, max_pt):
	return pt[0] >= min_pt and pt[0] <= max_pt and pt[1] >= min_pt and pt[1] <= max_pt

def get_border_tiles(sensor, max_bounds):
	border = set()
	min_y = sensor[1] - sensor[2] - 1
	max_y = sensor[1] + sensor[2] + 1
	for y in range(min_y, max_y + 1):
		if y == min_y or y == max_y:
			if in_bounds((sensor[0], y), 0, max_bounds):
				border.add((sensor[0], y))
			continue
		x_offset = (sensor[2] + 1) - abs(y - sensor[1])
		if in_bounds((sensor[0] - x_offset, y), 0, max_bounds):
			border.add((sensor[0] - x_offset, y))
		if in_bounds((sensor[0] + x_offset, y), 0, max_bounds):
			border.add((sensor[0] + x_offset, y))
	return border

def day_part2():
	sensors, beacons = parse_input()
	for i, sensor in enumerate(sensors):
		neighbors = get_intersecting_sensors(sensor, sensors)
		border = get_border_tiles(sensor, 4000000)
		for j, b in enumerate(border):
			print(f"Progress {i / len(sensors)}, {j / len(border)}")
			valid = True
			for neighbor in neighbors:
				if point_in_range(neighbor, b):
					valid = False
					break
			if valid:
				return b[0] * 4000000 + b[1]
	return "FAILED"

print(f"Part 1 answer: {str(day_part1())}")
print(f"Part 2 answer: {str(day_part2())}")
