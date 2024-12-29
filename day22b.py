import aoc, util
import numpy as np
import itertools as it

input = aoc.load_input(mode=aoc.MODE_LINES, dtype=int)

MASK = 0xFFFFFF

# 	Bit	0		1		2		3		4		5		6		7		8		9		10		11		12
# 1. 	-		-		-		-		-		-		0		1		2		3		4		5		6
# 2. 	5		6(+0)	7(+1)	8(+2)	9(+3)	10(+4)	11(+5)	12(+6)	13(+7)	14(+8)	15(+9)	16(+10)	17(+11)
# 3. 	-		-		-		-		-		-		-		-		-		-		-		0(+5)	1(+6)

def hash(value):
	value = (value ^ (value << 6)) & MASK
	value = (value ^ (value >> 5)) & MASK
	value = (value ^ (value << 11)) & MASK

	return value

patterns_per_seed = [ ]

for seed in input:
	value = seed
	prev_last_digit = value % 10

	pattern_cache = { } 

	pattern = ( -1, -1, -1, -1 )

	for i in range(2000):
		value = hash(value)

		last_digit = value % 10
		delta = last_digit - prev_last_digit
		prev_last_digit = last_digit
		
		pattern = (pattern[1], pattern[2], pattern[3], delta)

		if i >= 3 and not pattern in pattern_cache:
			pattern_cache[pattern] = last_digit

	patterns_per_seed.append(pattern_cache)

	print(f'{seed}: {len(pattern_cache)}')

def bananas_for_pattern(pattern):
	bananas = 0

	for banana_cache in patterns_per_seed:
		bananas_for_seed = banana_cache.get(pattern, 0)
		bananas += bananas_for_seed

	return bananas

best_pattern = None
most_bananas = None

for pattern in it.product(*it.repeat(range(-9, 10), 4)):
	if abs(sum(pattern)) >= 10:
		continue

	bananas = bananas_for_pattern(pattern)

	if best_pattern is None or bananas > most_bananas:
		best_pattern = pattern
		most_bananas = bananas

		print(f'New best! {most_bananas} bananas with pattern {best_pattern}')