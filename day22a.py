import aoc, util
import numpy as np

input = aoc.load_input(mode=aoc.MODE_LINES, dtype=int)

MASK = 0xFFFFFF

def hash(value):
	value = (value ^ (value << 6)) & MASK
	value = (value ^ (value >> 5)) & MASK
	value = (value ^ (value << 11)) & MASK

	return value

result = 0
for seed in input:
	value = seed

	for i in range(2000):
		value = hash(value)

	result += value

	print(f'{seed}: {value}')

print(result)