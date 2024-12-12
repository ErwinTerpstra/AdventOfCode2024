import aoc, util

def update_stone(stone, output):
	if stone == 0:
		output.append(1)
		return
	
	stone_str = str(stone)
	stone_len = len(stone_str)
	if stone_len % 2 == 0:
		output.append(int(stone_str[:stone_len // 2]))
		output.append(int(stone_str[stone_len // 2:]))
	else:
		output.append(stone * 2024)

stone_cache = { }
def blink(stone):
	if stone in stone_cache:
		return stone_cache.get(stone)
	
	new_stones = [ ]
	update_stone(stone, new_stones)

	stone_cache[stone] = new_stones
	return new_stones
	
count_cache = { }
def count_stones_after(stone, blinks):
	key = (stone, blinks)
	if key in count_cache:
		return count_cache[key]

	if blinks > 0:
		new_stones = blink(stone)
		count = sum((count_stones_after(substone, blinks - 1) for substone in new_stones))
	else:
		count = 1

	count_cache[key] = count
	return count

BLINKS = 75

input = aoc.load_input(mode=aoc.MODE_GRID, use_numpy=False, dtype=int, column_separator=' ')[0]
result = sum((count_stones_after(stone, BLINKS) for stone in input))

print(result)