import aoc
import re

input = aoc.load_input(mode=aoc.MODE_STRING)
matches = re.findall('mul\((\d+),(\d+)\)|do(n\'t)?\(\)', input)

result = 0
enable_mul = True
for lhs, rhs, op in matches:
	if lhs and rhs:
		if enable_mul:
			result += int(lhs) * int(rhs)
	else:
		enable_mul = op != 'n\'t'

print(result)