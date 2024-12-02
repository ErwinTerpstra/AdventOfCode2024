import aoc
import numpy as np

input = aoc.load_input(mode=aoc.MODE_GRID, use_numpy=True, dtype=int)
left = np.sort(input[:,0])
right = np.sort(input[:,1])
result = np.sum(np.abs(left - right))

print(result)