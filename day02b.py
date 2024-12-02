import aoc
import numpy as np

input = aoc.load_input(mode=aoc.MODE_GRID, use_numpy=True, numpy_axis=1, dtype=int)

def test_report(report):
	deltas = report[1:] - report[:-1]
	signs = np.sign(deltas)
	deltas = np.abs(deltas)
	desired_sign = signs[np.argmax(signs != 0)]

	invalid_levels = (signs != desired_sign) | (deltas == 0) | (deltas > 3)
	return not np.count_nonzero(invalid_levels)

safe_reports = 0
for report in input:
	is_safe = test_report(report)
	
	for i in range(len(report)):
		dampened_report = np.delete(report, i)
		is_safe = test_report(dampened_report)

		if is_safe:
			break

	if is_safe:
		safe_reports += 1

print(f'Safe reports: {safe_reports}')
		