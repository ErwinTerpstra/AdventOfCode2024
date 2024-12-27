import aoc, util
import numpy as np

input = aoc.load_input(mode=aoc.MODE_GRID, use_numpy=True, column_separator='')

start_pos = util.first_position(input == 'S')
goal_pos = util.first_position(input == 'E')

# Create distance field with distance to goal pos per cell
distance_field = np.full(input.shape, -1)

distance_field[goal_pos] = 0
pos_stack = [ goal_pos ]

while len(pos_stack) > 0:
	pos = pos_stack.pop()

	distance = distance_field[pos]

	neighbours = [ ]
	for dir in util.CARDINAL_DIRECTIONS:
		neighbour = pos + dir

		if not util.in_grid(neighbour, input.shape):
			continue

		not_wall = input[neighbour] != '#'
		not_set_yet = distance_field[neighbour] == -1

		if not_wall and not_set_yet:
			neighbours.append(neighbour)

	for neighbour in neighbours:
		distance_field[neighbour] = distance + 1

	pos_stack.extend(neighbours)

# For all walls, set the distance based on near non-wall path
for pos in util.all_coordinates(input.shape):
	if input[pos] != '#':
		continue

	def get_neighbour_distances(pos):
		for dir in util.CARDINAL_DIRECTIONS:
			neighbour = pos + dir
			if util.in_grid(neighbour, input.shape) and input[neighbour] != '#':
				yield distance_field[neighbour] + 1

	#print(list(get_neighbour_distances(pos)))
	min_distance = util.min_safe(*get_neighbour_distances(pos))

	if min_distance != None:
		distance_field[pos] = min_distance

shortest_path = distance_field[start_pos]

# Collect cheats by looking where entering a wall will shorten the path
cheats = [ ]
for pos in util.all_coordinates(input.shape):
	if input[pos] == '#':
		continue

	distance = distance_field[pos]

	for dir in util.CARDINAL_DIRECTIONS:
		neighbour = pos + dir

		# Only look for walls
		if not util.in_grid(neighbour, input.shape) or input[neighbour] != '#':
			continue

		neighbour_distance = distance_field[neighbour]
		delta = distance - neighbour_distance

		if delta > 1:
			cheats.append((neighbour, delta - 1))
		
grouped_cheats = util.groupby(cheats, lambda cheat: cheat[1])
print({ key: len(value) for key, value in grouped_cheats.items() })

result = sum((1 for cheat in cheats if cheat[1] >= 100))
print(result)
