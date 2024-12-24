import aoc, util
import numpy as np

input = aoc.load_input(mode=aoc.MODE_LINES)

towels = input[0].split(', ')
designs = input[2:]

cache = { towel: True for towel in towels }

def is_pattern_valid(pattern):
	if pattern in cache:
		return cache[pattern]
	
	if len(pattern) == 1:
		return False
	
	is_valid = False
	for i in range(len(pattern)):
		if is_pattern_valid(pattern[0:i]) and is_pattern_valid(pattern[i:]):
			is_valid = True
			break

	cache[pattern] = is_valid
	
	return is_valid

result = 0
for design in designs:
	is_valid = is_pattern_valid(design)

	print(f'Design {design} valid: {is_valid}')

	if is_valid:
		result += 1

print(result)