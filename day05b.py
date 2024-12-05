import aoc
import numpy as np

input = aoc.load_input(mode=aoc.MODE_LINES)

separator = input.index('')
rules = aoc.pairs_to_dict([ aoc.reversed_as_tuple(map(int, s.split('|'))) for s in input[:separator] ]) 
updates = [ list(map(int, s.split(','))) for s in input[separator+1:] ]

def first_broken_rule(update):
	for i, page in enumerate(update):
		dependency_indices = (update.index(d) for d in rules[page] if d in update)
		invalid_indices = [di for di in dependency_indices if di > i]

		if len(invalid_indices) > 0:
			return (i, min(invalid_indices))

	return None

def fix_update(update):
	while (pair := first_broken_rule(update)) is not None:
		update.insert(pair[0], update.pop(pair[1]))

	return update

fixed_updates = [ fix_update(update) for update in updates if first_broken_rule(update) is not None ]
result = sum([ update[len(update) // 2] for update in fixed_updates ])

print(result)