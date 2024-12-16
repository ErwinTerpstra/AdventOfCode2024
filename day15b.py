import aoc, util
import numpy as np

input = aoc.load_input(mode=aoc.MODE_STRING, remove_newlines=False)
parts = input.split('\n\n')

replace = \
[
	('#', '##'),
	('O', '[]'),
	('.', '..'),
	('@', '@.')
]

def replace_all(s):
	for src, dst in replace:
		s = s.replace(src, dst)

	return s

grid_lines = [ list(replace_all(line)) for line in parts[0].split('\n') ]

grid = np.array(grid_lines)
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

def can_push(from_pos, direction, boxes):
	next_pos = from_pos + direction
	next_tile = grid[next_pos]
	is_vertical = direction[0] != 0

	if next_tile == '#':
		return False
	
	if next_tile == '[' or next_tile == ']':
		if not can_push(next_pos, direction, boxes):
			return False
	
		other_pos = next_pos + (util.LEFT if next_tile == ']' else util.RIGHT)
		box_pos = next_pos if next_tile == '[' else other_pos

		boxes.add(box_pos)

		if is_vertical and not can_push(other_pos, direction, boxes):
			return False
		
	return True

def print_grid():
	grid[robot] = '@' 
	print(grid)
	grid[robot] = '.'

print_grid()
pushed_boxes = set()
for command in commands:
	direction = DIRECTIONS[command] 
	next_pos = robot + direction
	next_tile = grid[next_pos]

	pushed_boxes.clear()
	if can_push(robot, direction, pushed_boxes):
		for box_pos in pushed_boxes:
			grid[box_pos] = '.'
			grid[box_pos + util.RIGHT] = '.'

		for box_pos in pushed_boxes:
			grid[box_pos + direction] = '['
			grid[box_pos + direction + util.RIGHT] = ']'

		robot = next_pos
	
	print_grid()

# Count up GPS coordinates
result = 0
for pos in util.all_coordinates(grid.shape):
	if grid[pos] == '[':
		result += pos[0] * 100 + pos[1]

print(result)