import aoc
import re

input = aoc.load_input(mode=aoc.MODE_STRING)
matches = re.findall('mul\((\d+),(\d+)\)', input)
result = sum([ int(lhs) * int(rhs) for lhs, rhs in matches ])

print(result)