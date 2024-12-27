import aoc, util
import numpy as np
from tqdm import tqdm
from collections import deque

def flood_fill(start_pos, filter, max_distance = None):
	cur_frontier = [ start_pos ]
	next_frontier = [ ]

	while len(cur_frontier) > 0:
		while len(cur_frontier) > 0:
			pos = cur_frontier.pop()

			# Limit distance
			if max_distance is not None:
				delta = pos - start_pos
				if delta.manhattan() > max_distance:
					continue

			distance = distance_field[pos]

			for dir in util.CARDINAL_DIRECTIONS:
				neighbour = pos + dir

				if not util.in_grid(neighbour, input.shape):
					continue

				already_set = distance_field[neighbour] >= 0

				if not already_set and filter(neighbour):
					distance_field[neighbour] = distance + 1
					next_frontier.append(neighbour)

		cur_frontier, next_frontier = next_frontier, cur_frontier



input = aoc.load_input(mode=aoc.MODE_GRID, use_numpy=True, column_separator='')

start_pos = util.first_position(input == 'S')
goal_pos = util.first_position(input == 'E')

# Create distance field with distance to goal pos per cell
distance_field = np.full(input.shape, -1)
distance_field[goal_pos] = 0

flood_fill(goal_pos, lambda x: input[x] != '#')

# Next, flood fill outwards from each walkable node to fill wall nodes
walkable_nodes = sorted(util.all_positions(input != '#'), key=lambda node: distance_field[node])
for pos in walkable_nodes:
	flood_fill(pos, lambda x: input[x] == '#', max_distance=20)

print(input)
print(distance_field)

# Collect shortest path using distance field
shortest_path = [ start_pos ]
pos = start_pos
while pos != goal_pos:
	neighbours = ((n, distance_field[n]) for n in util.neighbours(pos, input.shape) if input[n] != '#')
	pos, d = util.min_item(neighbours, key=lambda pair: pair[1])
	shortest_path.append(pos)

# Collect cheats by for each path node, finding the positions at max 20 distane that could by reached by entering a wall
CHEAT_THRESHOLD = 100
cheats = { }

for pos in tqdm(shortest_path):
	distance = distance_field[pos]

	for neighbour in util.radius_around(pos, min_distance=2, max_distance=20, grid_size=input.shape):
		if input[neighbour] == '#':
			continue
		
		delta = neighbour - pos
		cheat_length = delta.manhattan()
		neighbour_distance = distance_field[neighbour]

		time_saved = distance - cheat_length - neighbour_distance

		# Only store cheats that actually saved time and end when they've just exited a wall
		if time_saved >= CHEAT_THRESHOLD:
			cheat_id = (pos, neighbour)
			cheats[cheat_id] = time_saved

grouped_cheats = util.groupby(cheats.items(), lambda cheat: cheat[1])
grouped_cheats = sorted(grouped_cheats.items(), key=lambda group: group[0])

for cheat_length, cheat_group in grouped_cheats:
	print(f'There are {len(cheat_group)} cheats that save {cheat_length} picoseconds')

print(f'In total {len(cheats)} cheats that save at least {CHEAT_THRESHOLD} picoseconds')