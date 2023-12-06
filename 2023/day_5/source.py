from pathlib import WindowsPath
import concurrent.futures

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
	
	group_mappings.reverse()
	
	seed_input = groups[0].split(': ')[1].split(' ')
	seed_ranges = [range(int(pair[0]), int(pair[0]) + int(pair[1])) for pair in zip(seed_input[::2], seed_input[1::2])]
	
	def get_src_seed(i, val):
		if len(group_mappings) == i + 2:
			for rng in seed_ranges:
				if val in rng:
					return val
			return None # not in seeds
		
		cur_val = val
		for group in group_mappings[i + 1:]:
			for mapping in group:
				if cur_val >= mapping['min_dest'] and cur_val <= mapping['max_dest']:
					cur_val -= mapping['diff']
					break

		for rng in seed_ranges:
			if cur_val in rng:
				return cur_val
		return None # not in seeds
	
	min_loc = 1000000000000000000
	for i, group in enumerate(group_mappings):
		for j, mapping in enumerate(group):
			for val in range(mapping['min_dest'], mapping['max_dest'] + 1):
				print(f"Group progress: {i / len(group_mappings) * 100}%\tMapping progress: {j / len(group_mappings) * 100}%\tVal progress: {val / mapping['max_dest'] * 100}%")
				src_seed = get_src_seed(i, val)
				if src_seed is not None and src_seed < min_loc:
					min_loc = val
	
	return min_loc

def translations():
	# temperature/humidity sets
	ths = [[0, 69, 1], [1, 0, 69]]
	# humidity/location sets
	hls = [[60, 56, 37], [56, 93, 4]]
	
	for th_set in ths:
		for hl_set in hls:
			range_min = max(th_set[1], hl_set[1])
			range_max = min(th_set[1] + th_set[2], hl_set[1] + hl_set[2])
			if range_min <= range_max:
				print(f"Overlap translation: {range_min} - {range_max}")
			lower_range_min = min(th_set[1], hl_set[1])
			print(f"Lower range: {lower_range_min} - {range_min - 1}")
			upper_range_max = max(th_set[1] + th_set[2], hl_set[1] + hl_set[2])
			print(f"Upper range: {range_max + 1} - {upper_range_max}")

print(part1())
#translations()
print(part2())
