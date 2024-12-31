import aoc, util
import numpy as np
import re

input = aoc.load_input(mode=aoc.MODE_LINES)

separator = input.index('')
signal_lines = input[:separator]
gate_lines = input[separator+1:]

signals = { }
gates = { }

for signal_line in signal_lines:
	name, level = re.search('(\\w+): (\\d)', signal_line).groups()
	signals[name] = int(level)

for gate_line in gate_lines:
	lhs, op, rhs, out = re.search('(\\w+) (\\w+) (\\w+) -> (\\w+)', gate_line).groups()
	gates[out] = (op, lhs, rhs)

result = 0
outputs = { s for s in (*signals.keys(), *gates.keys()) if s[0] == 'z' }

GATES = \
{
	'OR': lambda lhs, rhs: lhs | rhs,
	'XOR': lambda lhs, rhs: lhs ^ rhs,
	'AND': lambda lhs, rhs: lhs & rhs,
}

def get_level(name):
	if not name in signals:
		op, lhs, rhs = gates[name]

		level = GATES[op](get_level(lhs), get_level(rhs))
		signals[name] = level

	return signals[name]

for output in outputs:
	level = get_level(output)

	output_index = int(output[1:])
	result |= level << output_index

print(result)