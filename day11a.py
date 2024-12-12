import aoc, util
import numpy as np

def update_stone(stone):
	if stone == 0:
		return [ 1 ]
	
	stone_str = str(stone)
	stone_len = len(stone_str)
	if stone_len % 2 == 0:
		return [ int(stone_str[:stone_len // 2]), int(stone_str[stone_len // 2:]) ]
	
	return [ stone * 2024 ]

blink = lambda stones: [ new_stone for old_stone in stones for new_stone in update_stone(old_stone) ]

input = aoc.load_input(mode=aoc.MODE_GRID, use_numpy=False, dtype=int, column_separator=' ')[0]

for i in range(25):
	input = blink(input)
	print(f'After {i + 1} blinks, {len(input)} stones')