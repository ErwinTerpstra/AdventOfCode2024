import aoc, util
import re

input = aoc.load_input(mode=aoc.MODE_LINES, remove_empty=True)

clean_solution = lambda n: round(n) if (abs(n - round(n)) < 0.001) else None

result = 0
for line_a, line_b, line_price in zip(*(input[i::3] for i in range(3))):
	match_a = re.match('Button A: X\\+(\\d+), Y\\+(\\d+)', line_a)
	match_b = re.match('Button B: X\\+(\\d+), Y\\+(\\d+)', line_b)
	match_price = re.match('Prize: X=(\\d+), Y=(\\d+)', line_price)

	button_a = (int(match_a[1]), int(match_a[2]))
	button_b = (int(match_b[1]), int(match_b[2]))
	prize = (int(match_price[1]), int(match_price[2]))

	# na = (px - (bx/by) * py) / (ax - (bx/by) * ay)
	# nb = (py - (ay/ax) * px) / (by - (ay/ax) * bx)
	slope_a = button_a[1] / button_a[0]
	slope_b = button_b[0] / button_b[1]

	a_presses = clean_solution((prize[0] - slope_b * prize[1]) / (button_a[0] - slope_b * button_a[1]))
	b_presses = clean_solution((prize[1] - slope_a * prize[0]) / (button_b[1] - slope_a * button_b[0]))

	if a_presses is not None and b_presses is not None:
		result += a_presses * 3 + b_presses
	
print(result)