import aoc, util
import itertools, math
import numpy as np

input = aoc.load_input(mode=aoc.MODE_GRID, use_numpy=True, column_separator='')

antenna = ( (*pos, input[pos]) for pos in np.ndindex(*input.shape) if input[pos] != '.' )
antenna = { key: [ (int(pos[0]), int(pos[1])) for pos in group ] for key, group in util.groupby(antenna, lambda x: x[2]).items() }

antinodes = set()
for similar_antennas in antenna.values():
	for a, b in itertools.permutations(similar_antennas, 2):
		d = util.sub(b, a)
		gcd = math.gcd(d[0], d[1])
		d = util.div(d, gcd)
		
		p = b
		while util.in_grid(p, input.shape):
			antinodes.add(p)
			p = util.add(p, d)

result = len(antinodes)
print(result)