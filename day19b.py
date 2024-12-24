import aoc, util
import numpy as np

input = aoc.load_input(mode=aoc.MODE_LINES)

towels = input[0].split(', ')
designs = input[2:]

cache = {  }

def count_possibilities(pattern):
	if pattern in cache:
		return cache[pattern]
		
	possibilities = 0
	for towel in towels:
		if pattern.startswith(towel):
			remaining = pattern[len(towel):]
			possibilities += count_possibilities(remaining) if len(remaining) > 0 else 1
			
			#print(f'{pattern} - {pattern[0:i]}: {left}; {pattern[i:]}: {right}')

	cache[pattern] = possibilities
	
	return possibilities

print(towels)

result = 0
for design in designs:
	possibilities = count_possibilities(design)

	print(f'Design {design} possibilities: {possibilities}')

	result += possibilities

print(result)