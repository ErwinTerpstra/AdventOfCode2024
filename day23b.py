import aoc, util
import numpy as np
import itertools as it
from collections import defaultdict

input = aoc.load_input(mode=aoc.MODE_GRID, column_separator='-', row_type=tuple)

computers = set()
connections = defaultdict(set)

for pair in input:
	computers.update(pair)

	connections[pair[0]].add(pair[1])
	connections[pair[1]].add(pair[0])

cliques = util.bron_kerbosch(computers, connections)
max_clique = util.max_item(cliques, key=lambda x: len(x))

print(','.join(sorted(max_clique)))