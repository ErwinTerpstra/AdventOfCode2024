import aoc, util
import re

input = aoc.load_input(mode=aoc.MODE_LINES, remove_empty=True)
map_size = (11, 7) if aoc.input_type() == 'example' else (101, 103)

# Parse robots
robots = [ ]
for line in input:
	match = re.match('p=(\\-?\\d+),(\\-?\\d+) v=(\\-?\\d+),(\\-?\\d+)', line)

	p = (int(match[1]), int(match[2]))
	v = (int(match[3]), int(match[4]))

	robots.append((p, v))

# Calculate positions at T=100
positions = [ ]
for p, v in robots:
	p_prime = util.mod(util.add(p, util.mul(v, 100)), map_size)
	positions.append(p_prime)

# Print map
for y in range(map_size[1]):
	for x in range(map_size[0]):
		n = positions.count((x, y))
		print(str(n) if n > 0 else '.', end='')

	print()

# Count quadrants
quadrant_size = util.div(map_size, 2)
quadrants = [ tuple((0 if x < max else 1 for x, max in zip(p, quadrant_size))) for p in positions if p[0] != quadrant_size[0] and p[1] != quadrant_size[1] ]

tl = quadrants.count((0, 0))
tr = quadrants.count((1, 0)) 
bl = quadrants.count((0, 1))
br = quadrants.count((1, 1))
result = tl * tr * bl * br

print(tl, tr, bl, br)
print(result)