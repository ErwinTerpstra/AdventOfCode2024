import aoc
import numpy as np

input = aoc.load_input(mode=aoc.MODE_GRID, use_numpy=True, column_separator='')

position = np.array(np.where(input == '^')).flatten()
direction = np.array([-1, 0])

is_valid_position = lambda pos, size: pos[0] >= 0 and pos[1] >= 0 and pos[0] < size[0] and pos[1] < size[1]

while True:
	input[tuple(position)] = 'X'

	next_position = position + direction
	if not is_valid_position(next_position, input.shape):
		break

	if input[tuple(next_position)] == '#':
		direction[0], direction[1] = direction[1], -direction[0]
	else:
		position = next_position

result = np.count_nonzero(input == 'X')

print(result)