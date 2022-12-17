from pathlib import WindowsPath
import re
from dijkstra import Graph, DijkstraSPF
import itertools

input_path = WindowsPath(__file__).parent / 'day16.txt'

class Valve:
	def __init__(self, label, flow_rate, labeled_neighbors):
		self.label = label
		self.flow_rate = flow_rate
		self.labeled_neighbors = labeled_neighbors
		self.open = False
	
	def __eq__(self, other):
		return self.label == other.label
		
	def __hash__(self):
		return hash(self.label)
	
	def calc_distances(self, graph : Graph, flow_valves : list):
		self.dists = dict()
		dijkstra = DijkstraSPF(graph, self)
		for valve in flow_valves:
			if valve == self:
				continue
			self.dists[valve.label] = dijkstra.get_distance(valve) + 1

def parse_input():
	input = ''
	with open(input_path) as f:
		input = f.readlines()
	valves = dict()
	for line in input:
		if line == '\n':
			continue
		label = line[6:8]
		flow_rate = [int(s) for s in re.findall(r'-?\d+\.?\d*', line)][0]
		if 'valves' in line:
			neighbors = line.strip().split('valves ')[1].split(', ')
		else:
			neighbors = [line.strip().split('valve ')[1]]
		valves[label] = Valve(label, flow_rate, neighbors)
	return valves

def find_optimal_route(start : Valve, flow_valves: set, min_left: int, graph: Graph):
	if min_left <= 0:
		return 0, []
	
	max_value = 0
	best_route = []

	flow_valves.remove(start)
	for valve in flow_valves:
		time_to_open = start.dists[valve.label]
		value, route = find_optimal_route(valve, flow_valves.copy(), min_left - time_to_open, graph)
		if value > max_value:
			max_value = value
			best_route = route
	max_value += start.flow_rate * min_left
	best_route.insert(0, start.label)
	return max_value, best_route

def day_part1():
	valves = parse_input()
	graph = Graph()
	for valve in valves.values():
		for neighbor in valve.labeled_neighbors:
			graph.add_edge(valve, valves[neighbor], 1)
	flow_valves = set([x for x in valves.values() if x.flow_rate > 0])
	flow_valves.add(valves['AA'])
	for valve in flow_valves:
		valve.calc_distances(graph, flow_valves)
	
	best_route = find_optimal_route(valves['AA'], flow_valves, 30, graph)
	return best_route[0]

def find_permutations_in_timeframe(str_path : list, str_valid_valves : list, time_left : int, value : int, all_valves : dict, perm_list : list):
	str_root = str_path[-1]
	str_valid_valves.remove(str_root)
	for str_valve in str_valid_valves:
		cur_time_left = time_left - all_valves[str_root].dists[all_valves[str_valve].label]
		new_path = str_path.copy()
		new_path.append(str_valve)
		if cur_time_left >= 0:
			find_permutations_in_timeframe(new_path, str_valid_valves.copy(), cur_time_left, value + all_valves[str_valve].flow_rate * cur_time_left, all_valves, perm_list)
	perm_list.append(dict(path=str_path[1:], value=value))

def find_valid_routes_part2(flow_valves : list, duration : int, all_valves : dict):
	flow_valves = flow_valves.copy()
	str_valves = [valve.label for valve in flow_valves]
	
	perms_within_timeframe = []
	find_permutations_in_timeframe(['AA'], str_valves, 26, 0, all_valves, perms_within_timeframe)
	print(f"Found perms within timeframe: {len(perms_within_timeframe)}")

	max_value = 0
	perm_count = len(perms_within_timeframe)
	loop_count = perm_count ** 2
	for i, p_a in enumerate(perms_within_timeframe):
		for j, p_b in enumerate(perms_within_timeframe[i + 1:]):
			if p_a == p_b:
				continue
			# Ignore permutations where we attempt to activate the same valve (list intersection)
			if len(set(p_a['path']) & set(p_b['path'])) > 0:
				continue
			print(f"Progress {(i * perm_count + j) / loop_count}")
			cur_value = p_a['value'] + p_b['value']
			if cur_value > max_value:
				max_value = cur_value
	return max_value

def day_part2():
	valves = parse_input()
	graph = Graph()
	for valve in valves.values():
		for neighbor in valve.labeled_neighbors:
			graph.add_edge(valve, valves[neighbor], 1)
	flow_valves = set([x for x in valves.values() if x.flow_rate > 0])
	flow_valves.add(valves['AA'])
	for valve in flow_valves:
		valve.calc_distances(graph, flow_valves)
	return find_valid_routes_part2(flow_valves, 26, valves)

print(f"Part 1 answer: {str(day_part1())}")
print(f"Part 2 answer: {str(day_part2())}")
