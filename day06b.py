import aoc
import numpy as np

input = aoc.load_input(mode=aoc.MODE_GRID, use_numpy=True, column_separator='')

start_pos = tuple(( p[0] for p in np.where(input == '^') ))
position = start_pos
direction = (-1, 0)

is_valid_position = lambda pos, size: pos[0] >= 0 and pos[1] >= 0 and pos[0] < size[0] and pos[1] < size[1]
add_pos = lambda a, b: (a[0] + b[0], a[1] + b[1])
rot90 = lambda dir: (dir[1], -dir[0])

def step(position, direction):
	next_position = add_pos(position, direction)
	if not is_valid_position(next_position, input.shape):
		return (False, next_position, direction)

	if input[next_position] == '#':
		return (True, position, rot90(direction))
	else:
		return (True, next_position, direction)
	
def would_cause_loop(obstacle_pos, position, direction, visited_locations):
	input[obstacle_pos] = '#'
	direction = rot90(direction)

	while True:
		visited_locations.add((position, direction))
		in_grid, position, direction = step(position, direction)

		if not in_grid:
			break
		
		if (position, direction) in visited_locations:
			break

	input[obstacle_pos] = '.'
	return in_grid

# Create initial path
path = [ ]
while True:
	path.append((position, direction))
	in_grid, position, direction = step(position, direction)

	if not in_grid:
		break

# Find places for obstacles
obstacle_locations = set()
tried_locations = set()

N = len(path) - 1
for i in range(N):
	print(f'{i}/{N-1}')

	position, direction = path[i]
	next_position, next_direction = path[i + 1]

	# If the next position hasn't moved it means there already was an obstacle in front of us
	# Also skip start position
	if position == next_position or position == start_pos:
		continue

	# Skip locations that we already attempted
	if next_position in tried_locations:
		continue

	# Check if placing an obstacle in the way here would cause a loop
	if would_cause_loop(next_position, position, direction, set(path[:i+1])):
		obstacle_locations.add(next_position)

	tried_locations.add(next_position)

result = len(obstacle_locations)
print(result)