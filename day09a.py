import aoc, util
import itertools

input = aoc.load_input(mode=aoc.MODE_GRID, use_numpy=False, dtype=int, column_separator='')[0]
if len(input) % 2 == 1:
	input.append(0)

map = [ ]
for file_id, (file_size, free_space) in enumerate(zip(input[::2], input[1::2])):
	map.extend([ file_id ] * file_size)
	map.extend([ -1 ] * free_space)

free_idx = 0
block_idx = len(map) - 1

while block_idx > free_idx:
	if map[block_idx] == -1:
		block_idx -= 1
		continue

	if map[free_idx] == -1:
		map[free_idx], map[block_idx] = map[block_idx], -1
		block_idx -= 1

	free_idx += 1

result = sum((i * id for i, id in enumerate(map) if id >= 0))
print(result)