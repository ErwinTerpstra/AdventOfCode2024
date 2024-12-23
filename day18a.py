import aoc, util
import numpy as np

input = aoc.load_input(mode=aoc.MODE_GRID, dtype=int, column_separator=',')

grid_size = util.Point((7,7) if aoc.input_type() == 'example' else (71,71))
num_bytes = 12 if aoc.input_type() == 'example' else 1024

start_pos = util.ZERO
goal_pos = grid_size - util.ONE

grid = np.zeros(grid_size, dtype=bool)

for x, y in input[:num_bytes]:
	grid[(y, x)] = True

for y in range(grid_size[0]):
	for x in range(grid_size[1]):
		print('#' if grid[(y, x)] else '.', end='')

	print()

### Pathfind

class Node:
	def __init__(self, pos, parent = None):
		self.pos = pos
		self.dir = dir
		self.parent = parent

		if parent is not None:
			self.g = parent.g + 1
		else:
			self.g = 0

		delta = goal_pos - pos
		self.h = sum((x for x in delta))
		self.f = self.g + self.h

	def neighbours(self):
		for dir in util.CARDINAL_DIRECTIONS:
			yield Node(self.pos + dir, self)

open_list = { start_pos: Node(start_pos) }
closed_list = { }
found_path = False
	
while len(open_list) > 0:
	node_t, node = util.min_item(open_list.items(), lambda x: x[1].f)
	del open_list[node_t]

	# Add to closed list
	closed_list[node.pos] = node

	if node.pos == goal_pos:
		found_path = True
		break

	# Find neighbours
	for neighbour in node.neighbours():
		if not util.in_grid(neighbour.pos, grid_size) or grid[neighbour.pos]:
			continue

		# Check if we have it already on the closed list
		if neighbour.pos in closed_list and closed_list[neighbour.pos].g < neighbour.g:
			continue
		
		# Check if we have an existing cheaper one on the open list
		if neighbour.pos in open_list:
			existing_node = open_list[neighbour.pos]

			# If existing node is cheaper, skip neighbour
			if existing_node.g < neighbour.g:
				continue
		
		# If not present yet, or neighbour is cheaper, add to open list
		open_list[neighbour.pos] = neighbour

print(node.g)