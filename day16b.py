import aoc, util
import numpy as np
import os

def print_grid(node):
	buffer = [ ]
	for y in range(input.shape[0]):
		buffer.append('|')

		for x in range(input.shape[1]):
			pos = (y, x)

			if any((n.pos == pos for n in open_list.values())):
				buffer.append('+')
			else:
				buffer.append(input[pos])

		buffer.append('|')
		buffer.append('\n')

	buffer_str = ''.join(buffer)
	
	os.system('cls')
	print(buffer_str, flush=True)
	print(f'Open list: {len(open_list)}; Closed list: {len(closed_list)}')

class Node:
	def __init__(self, pos, dir, g_d = 0, parent = None):
		self.pos = pos
		self.dir = dir
		self.parents = [ ]

		if parent is not None:
			self.parents.append(parent)

		self.g = (parent.g if parent is not None else 0) + g_d

		delta = goal_pos - pos
		
		self.h = sum((x for x in delta))

		#self.h = 0

		self.f = self.g + self.h

	def neighbours(self):
		front = Node(self.pos + self.dir, self.dir, 1, self)
		left = Node(self.pos, self.dir.rotCCW(), 1000, self)
		right = Node(self.pos, self.dir.rotCW(), 1000, self)

		return ( front, left, right )

input = aoc.load_input(mode=aoc.MODE_GRID, use_numpy=True, column_separator='')

start_pos = util.Point((l[0] for l in np.where(input == 'S')))
goal_pos = util.Point((l[0] for l in np.where(input == 'E')))

open_list = { start_pos: Node(start_pos, util.RIGHT) }
closed_list = { }

shortest_paths = [ ]
shortest_length = None

nodes_visited = 0
while len(open_list) > 0:
	node_t, node = util.min_item(open_list.items(), lambda x: x[1].f)
	del open_list[node_t]

	nodes_visited += 1

	# if nodes_visited % 1000 == 0:
	# 	print_grid(node)
	# 	print(nodes_visited)

	if shortest_length is not None and node.g > shortest_length:
		break

	# Add to closed list
	t = (node.pos, node.dir)
	if t in closed_list:
		closed_list[t] = util.min_safe(closed_list[t], node.g)
	else:
		closed_list[t] = node.g

	# Check if is target
	if node.pos == goal_pos:
		shortest_length = node.g			
		shortest_paths.append(node)
		print(f'Found path; cost: {node.g}')
		continue

	# Find neighbours
	for neighbour in node.neighbours():
		if input[neighbour.pos] == '#':
			continue

		if shortest_length is not None and neighbour.g > shortest_length:
			continue

		# Check if we have it already on the closed list
		neighbour_transform = (neighbour.pos, neighbour.dir)
		if neighbour_transform in closed_list and closed_list[neighbour_transform] < neighbour.g:
			continue

		# Check if we have an existing cheaper one on the open list
		if neighbour_transform in open_list:
			existing_node = open_list[neighbour_transform]

			# If existing node is cheaper, skip neighbour
			if existing_node.g < neighbour.g:
				continue

			# If exactly the same cost, add to parents list
			if existing_node.g == neighbour.g:
				existing_node.parents.append(node)
				continue
		
		# If not present yet, or neighbour is cheaper, add to open list
		open_list[neighbour_transform] = neighbour

path_nodes = set()
for node in shortest_paths:
	node_buffer = [ node ]
	while len(node_buffer) > 0:
		node = node_buffer.pop()
		path_nodes.add(node.pos)

		node_buffer.extend(node.parents)

print(len(path_nodes))