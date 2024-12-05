import aoc
import numpy as np

input = aoc.load_input(mode=aoc.MODE_LINES)

separator = input.index('')

rules = aoc.pairs_to_dict([ tuple(map(int, s.split('|'))) for s in input[:separator] ]) 
updates = [ list(map(int, s.split(','))) for s in input[separator+1:] ]

is_update_valid = lambda update, rules: all(( update.index(d) > i for i, p in enumerate(update) for d in rules[p] if d in update))
result = sum([ update[len(update) // 2] for update in updates if is_update_valid(update, rules) ])

print(result)