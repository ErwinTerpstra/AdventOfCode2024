import aoc, util
import itertools
import numpy as np

input = aoc.load_input(mode=aoc.MODE_GRID, use_numpy=True, column_separator='')

antenna = ( (*pos, input[pos]) for pos in np.ndindex(*input.shape) if input[pos] != '.' )
antenna = { key: [ (int(pos[0]), int(pos[1])) for pos in group ] for key, group in util.groupby(antenna, lambda x: x[2]).items() }

antinodes = set()
for similar_antennas in antenna.values():
	candidates = ( util.add(b, util.sub(b, a)) for a, b in itertools.permutations(similar_antennas, 2) )
	antinodes.update(( pos for pos in candidates if util.in_grid(pos, input.shape) ))

result = len(antinodes)
print(result)