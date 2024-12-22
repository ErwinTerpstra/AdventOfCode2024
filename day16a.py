import aoc, util
import numpy as np
import bisect 

class Node:
	def __init__(self, pos, dir, g_d = 0, parent = None):
		self.pos = pos
		self.dir = dir
		self.parent = parent


		self.g = (parent.g if parent is not None else 0) + g_d
		self.h = 0		

		self.f = self.g + self.h

	def neighbours(self):
		front = Node(self.pos + self.dir, self.dir, 1, self)
		left = Node(self.pos, self.dir.rotCCW(), 1000, self)
		right = Node(self.pos, self.dir.rotCW(), 1000, self)

		return ( front, left, right )

input = aoc.load_input(mode=aoc.MODE_GRID, use_numpy=True, column_separator='')

start_pos = util.Point((l[0] for l in np.where(input == 'S')))
goal_pos = util.Point((l[0] for l in np.where(input == 'E')))

open_list = [ Node(start_pos, util.RIGHT) ]
closed_list = { }
found_path = False
	
while len(open_list) > 0:
	node = open_list.pop(-1)

	# Add to closed list
	closed_list[(node.pos, node.dir)] = node

	if node.pos == goal_pos:
		found_path = True
		break

	# Find neighbours
	for neighbour in node.neighbours():
		if input[neighbour.pos] == '#':
			continue

		neighbour_transform = (neighbour.pos, neighbour.dir)

		# Check if we have it already on the closed list
		if neighbour_transform in closed_list and closed_list[neighbour_transform].g < neighbour.g:
			continue

		# Check if we have an existing one on the open list
		existing_index = util.index(open_list, neighbour_transform, lambda node: (node.pos, node.dir))
		if existing_index >= 0:
			if open_list[existing_index].g < neighbour.g:
				continue

			open_list[existing_index] = neighbour
			
			# "Bubble down" the newly replaced element until it is the correct spot
			i = existing_index
			while i > 0 and open_list[i].f >  open_list[i - 1].f:
				(open_list[i], open_list[i - 1]) = (open_list[i - 1], open_list[i])
				i -= 1
		else:
			bisect.insort(open_list, neighbour, key=lambda node: -node.f)


print(node.g)