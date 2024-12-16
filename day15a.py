import aoc, util
import numpy as np

input = aoc.load_input(mode=aoc.MODE_STRING, remove_newlines=False)
parts = input.split('\n\n')

grid = np.array([ list(line) for line in parts[0].split('\n') ])
commands = list(parts[1].replace('\n',''))

# Get robot from grid, and replace with empty space
robot = util.Point((l[0] for l in np.where(grid == '@')))
grid[robot] = '.'

DIRECTIONS = \
{
	'^': util.UP,
	'v': util.DOWN,
	'<': util.LEFT,
	'>': util.RIGHT
}

def find_free_space(pos, direction):
	while util.in_grid(pos, grid.shape):
		if grid[pos] == '.':
			return pos
		
		if grid[pos] == '#':
			return None
		
		pos += direction

	# Shouldn't happen if there's walls around the grid
	return None

for command in commands:
	direction = DIRECTIONS[command] 
	next = robot + direction

	# Empty space, move into it
	if grid[next] == '.':
		robot = next
		continue

	# Wall, stop moving
	if grid[next] == '#':
		continue

	# Box, check if we can push it
	if grid[next] =='O':
		free_pos = find_free_space(next, direction)

		if free_pos is not None:
			# Move stack of boxes
			grid[next] = '.'
			grid[free_pos] = 'O'

			# Move robot in newly formed free space
			robot = next

		continue

	raise 'Unexpected grid cell'

# Count up GPS coordinates
result = 0
for pos in util.all_coordinates(grid.shape):
	if grid[pos] == 'O':
		result += pos[0] * 100 + pos[1]

print(result)