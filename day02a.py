import aoc
import numpy as np

input = aoc.load_input(mode=aoc.MODE_GRID, use_numpy=True, numpy_axis=1, dtype=int)

safe_reports = 0
for report in input:
	deltas = report[1:] - report[0:-1]
	signs = np.sign(deltas)
	deltas = np.abs(deltas)

	if np.all(signs == signs[0]) and np.all((deltas >= 1) & (deltas <= 3)):
		safe_reports += 1

print(f'Safe reports: {safe_reports}')
		