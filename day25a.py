import aoc, util
import numpy as np
import itertools as it

input = aoc.load_input(mode=aoc.MODE_LINES)

keys = [ ]
locks = [ ]

count_height = lambda a: np.where(a == '.')[0][0] - 1
convert_to_heights = lambda a: np.array([ count_height(a[:,column]) for column in range(a.shape[1]) ])

block_start = 0
while block_start < len(input):
	try:
		block_end = input.index('', block_start+1)
	except:
		block_end = len(input)

	block = np.array([ list(line) for line in input[block_start:block_end] ])
	is_lock = block[(0, 0)] == '#'

	heights = convert_to_heights(block if is_lock else np.flipud(block))
	if is_lock:
		locks.append(heights)
	else:
		keys.append(heights)

	block_start = block_end + 1

result = 0
for key, lock in it.product(keys, locks):
	sum = key + lock
	overlap = len(np.where(sum >= 6)[0]) > 0

	if not overlap:
		result += 1

print(result)