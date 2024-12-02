import aoc
import numpy as np

input = aoc.load_input(mode=aoc.MODE_GRID, use_numpy=True, dtype=int)
counts = dict(zip(*np.unique(input[:,1], return_counts=True)))
result = sum((x * counts.get(x, 0) for x in input[:,0]))

print(result)