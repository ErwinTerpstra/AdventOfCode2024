import aoc, util
import numpy as np
import itertools as it

input = aoc.load_input(mode=aoc.MODE_GRID, column_separator='-', row_type=tuple)

computers = set()
connections = set()

for pair in input:
	computers.update(pair)

	connections.add(util.sort_tuple(pair))

print(computers)
print(connections)

result = 0
for triad in it.combinations(computers, 3):
	if not triad[0][0] == 't' and not triad[1][0] == 't' and not triad[2][0] == 't':
		continue

	pc1, pc2, pc3 = util.sort_tuple(triad)

	if (pc1, pc2) in connections and (pc1, pc3) in connections and (pc2, pc3) in connections:
		result += 1

print(result)