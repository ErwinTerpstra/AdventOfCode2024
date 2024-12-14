import aoc, util
import numpy as np

input = aoc.load_input(mode=aoc.MODE_GRID, use_numpy=True, column_separator='')
areas = np.full(input.shape, -1, dtype=int)
area_coordinates = [ ]

def flood_fill(pos, area_id = -1):
	# Area already visited
	if areas[pos] != -1:
		return

	plant_type = input[pos]	

	# If we want to create a new area, register an ID
	if area_id == -1:
		area_id = len(area_coordinates)
		area_coordinates.append([ ])

	areas[pos] = area_id
	area_coordinates[area_id].append(pos)

	# Propogate to neighbours
	for offset in util.CARDINAL_DIRECTIONS:
		neighbour = util.add(pos, offset)

		if util.in_grid(neighbour, input.shape) and input[neighbour] == plant_type:
			flood_fill(neighbour, area_id)

# Generate area map
for pos in util.all_coordinates(input.shape):
	flood_fill(pos)

# Calculate perimeter size
perimeters = np.full(len(area_coordinates), 0, int)
for pos in util.all_coordinates(input.shape):
	area_id = areas[pos]

	for offset in util.CARDINAL_DIRECTIONS:
		neighbour = util.add(pos, offset)

		if not util.in_grid(neighbour, input.shape) or areas[neighbour] != area_id:
			perimeters[area_id] += 1

# Calculate sum of fence prices as perimeter length * surface area
result = sum((perimeters[area_id] * len(area_coordinates[area_id]) for area_id in range(len(area_coordinates))))
print(result)