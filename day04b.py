import aoc
import numpy as np
from itertools import product

input = aoc.load_input(mode=aoc.MODE_GRID, use_numpy=True, column_separator='')

match_mas = lambda a: (a[0] == 'M' and a[2] == 'S') or (a[0] == 'S' and a[2] == 'M')
is_match = lambda grid: match_mas(np.diag(grid)) and match_mas(np.diag(np.fliplr(grid)))
slice_33 = lambda grid, c: grid[c[0]-1:c[0]+2,c[1]-1:c[1]+2]

centers = product(range(1, input.shape[0] - 1), range(1, input.shape[1] - 1))
centers = [ c for c in centers if input[c] == 'A' ]

result = sum([ 1 for c in centers if is_match(slice_33(input, c)) ])

print(result)