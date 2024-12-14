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

# Calculate list of sides per area
determine_area = lambda pos: areas[pos] if util.in_grid(pos, areas.shape) else -1

corners = np.zeros(len(area_coordinates), dtype=int)
for pos in util.all_coordinates(input.shape, padding=-1):
	origin = determine_area(util.add(pos, util.ZERO))
	left = determine_area(util.add(pos, util.RIGHT))
	right = determine_area(util.add(pos, util.DOWN))
	front = determine_area(util.add(pos, util.ONE))

	for r in range(4):
		if origin != -1:
			convex_corner = front != origin and left != origin and right != origin
			concave_corner = front != origin and left == origin and right == origin
			inner_corner = front == origin and left != origin and right != origin

			if convex_corner or concave_corner or inner_corner:
				corners[origin] += 1

		# Rotate for next iteration
		(origin, left, front, right) = (left, front, right, origin)


# Calculate sum of fence prices as number of sides * surface area
result = sum(corners[area_id] * len(area_coordinates[area_id]) for area_id in range(len(area_coordinates)))
print(result)