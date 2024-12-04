import aoc
import numpy as np

MATCH = 'XMAS'

words_from_row = lambda row, length: [ ''.join(values) for values in zip(*[ row[i:] for i in range(length) ]) ]
all_diagonals = lambda grid: [ np.diagonal(grid, offset=i) for i in range(-grid.shape[0] + 1, grid.shape[1]) ]
words_from_grid = lambda rows, word_length: [ word for row in rows for word in words_from_row(row, word_length) ]

input = aoc.load_input(mode=aoc.MODE_GRID, use_numpy=True, column_separator='')
orientations = (input, input.T, all_diagonals(input), all_diagonals(np.fliplr(input)))
all_words = [ word for grid in orientations for word in words_from_grid(grid, len(MATCH)) ]
result = all_words.count(MATCH) + all_words.count(MATCH[::-1])

print(result)