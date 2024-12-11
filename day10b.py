import aoc, util
import numpy as np

NEIGHBOURS = [ (-1, 0), (1, 0), (0, -1), (0, 1) ]

input = aoc.load_input(mode=aoc.MODE_GRID, use_numpy=True, dtype=int, column_separator='')
trailheads = list(zip(*np.where(input == 0)))

trail_scores = [ ]
for position in trailheads:
	open_list = [ position ]
	score = 0

	while len(open_list) > 0:
		position = open_list.pop()

		level = input[position]

		if level == 9:
			score += 1
			continue

		for offset in NEIGHBOURS:
			neighbour = util.add(position, offset)

			if util.in_grid(neighbour, input.shape) and input[neighbour] == level + 1:
				open_list.append(neighbour)
	
	trail_scores.append(score)

result = sum(trail_scores)
print(result)