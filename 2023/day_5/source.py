from pathlib import WindowsPath
import concurrent.futures
from multiprocessing import Process, Queue

input_path = WindowsPath(__file__).parent / 'input.txt'

def part1():
	input = ''
	with open(input_path) as f:
		input = f.read()
	
	groups = input.split('\n\n')
	seeds = groups[0].split(': ')[1].split(' ')
	group_mappings = []
	for group in groups:
		mappings = []
		for ln in group.split('\n'):
			if ':' in ln:
				continue
			min_dest =  int(ln.split(' ')[0])
			min_src = int(ln.split(' ')[1])
			range_len = int(ln.split(' ')[2])
			mappings.append({
				'min_src': min_src,
				'max_src': min_src + range_len,
				'diff': min_dest - min_src
			})
		group_mappings.append(mappings)
	
	locations = []
	for seed in seeds:
		cur_val = int(seed)
		for group in group_mappings:
			for mapping in group:
				if cur_val >= mapping['min_src'] and cur_val <= mapping['max_src']:
					cur_val += mapping['diff']
					break
		locations.append(cur_val)
	
	return min(locations)

def brute_force_baby(seed_range, best_num_group, group_mappings):
	lowest_loc = 100000000000000000
	best_seed = 0
	for i, seed in enumerate(seed_range):
		cur_val = int(seed)
		for group in group_mappings:
			for mapping in group:
				if cur_val >= mapping['min_src'] and cur_val <= mapping['max_src']:
					cur_val += mapping['diff']
					break
		if cur_val < lowest_loc:
			lowest_loc = cur_val
			best_seed = seed
		if i % 1000000 == 0:
			print(f"seed group progress {i / len(seed_range)}%, best so far {lowest_loc}, best seed {best_seed}")
	best_num_group.put(lowest_loc)
	return lowest_loc

def part2():
	input = ''
	with open(input_path) as f:
		input = f.read()
	
	groups = input.split('\n\n')
	group_mappings = []
	for group in groups:
		mappings = []
		for ln in group.split('\n'):
			if ':' in ln:
				continue
			min_dest =  int(ln.split(' ')[0])
			min_src = int(ln.split(' ')[1])
			range_len = int(ln.split(' ')[2])
			mappings.append({
				'min_src': min_src,
				'max_src': min_src + range_len,
				'diff': min_dest - min_src,
				'min_dest': min_dest,
				'max_dest': min_dest + range_len
			})
		group_mappings.append(mappings)
	
	seed_input = groups[0].split(': ')[1].split(' ')
	seed_ranges = [range(int(pair[0]), int(pair[0]) + int(pair[1])) for pair in zip(seed_input[::2], seed_input[1::2])]
	
	processes = []
	best_nums = Queue()
	for i, seed_rng in enumerate(seed_ranges):
		p = Process(target=brute_force_baby, args=(seed_rng, best_nums, group_mappings))
		processes.append(p)
		p.start()
    
	for p in processes:
		p.join()
	
	best_num_list = []
	while not best_nums.empty():
		best_num_list.append(best_nums.get())
	
	print(f"All best nums: {best_num_list}")
	
	# off by one??
	return min(best_num_list)

print(part1())
if __name__ == '__main__':  
	print(part2())
