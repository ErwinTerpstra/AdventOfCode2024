import aoc, util
import numpy as np
import re

from collections import defaultdict

input = aoc.load_input(mode=aoc.MODE_LINES)

separator = input.index('')
signal_lines = input[:separator]
gate_lines = input[separator+1:]

signals = { }
gates = { }
signal_gates = defaultdict(set)
gate_labels = defaultdict(set)
invalid_gates = set()

for signal_line in signal_lines:
	name, level = re.search('(\\w+): (\\d)', signal_line).groups()
	signals[name] = int(level)

for gate_line in gate_lines:
	lhs, op, rhs, out = re.search('(\\w+) (\\w+) (\\w+) -> (\\w+)', gate_line).groups()
	gates[out] = (op, lhs, rhs)

	signal_gates[lhs].add(out)
	signal_gates[rhs].add(out)

find_gates = lambda first_char: { s for s in (*signals.keys(), *gates.keys()) if s[0] == first_char }

def find_gate(items, op): 
	return next((gate for gate in items if gates[gate][0] == op), None)

def find_common_gate(lhs, rhs, op):
	common_gates = signal_gates[lhs] & signal_gates[rhs]
	gate = find_gate(common_gates, op)

	if gate is not None:
		return (gate, True, True)
	
	left_gate = find_gate(signal_gates[lhs], op)
	right_gate = find_gate(signal_gates[rhs], op)

	if left_gate is not None:
		if right_gate is not None:
			# Both are connected to a different gate of the correct type, tricky to determine the correct one
			assert(False)
			return ((left_gate, right_gate), True, True)
		else:
			# Left gate is probably the correct one
			return (left_gate, True, False)
	else:
		if right_gate is not None:
			# Right gate is probably the correct one
			return (right_gate, False, True)
		else:
			return (None, False, False)

def label_gate(lhs, rhs, op, label):
	gate, lhs_valid, rhs_valid = find_common_gate(lhs, rhs, op)
	
	if not lhs_valid:
		invalid_gates.add(lhs)

	if not rhs_valid:
		invalid_gates.add(rhs)

	if gate is not None:
		gate_labels[gate].add(label)

	return gate

def verify_half_adder(bit_index, lhs, rhs, out):
	sum = label_gate(lhs, rhs, 'XOR', f'bit{bit_index:02}_XOR1')
	carry_out = label_gate(lhs, rhs, 'AND', f'bit{bit_index:02}_AND1')

	assert(sum is not None)
	assert(carry_out is not None)

	if sum != out:
		invalid_gates.add(sum)

	return carry_out

def verify_full_adder(bit_index, lhs, rhs, carry_in, out):
	sum_inner = label_gate(lhs, rhs, 'XOR', f'bit{bit_index:02}_XOR1')
	carry_inner1 = label_gate(lhs, rhs, 'AND', f'bit{bit_index:02}_XOR1')
	assert(sum_inner is not None and carry_inner1 is not None)

	sum = label_gate(sum_inner, carry_in, 'XOR', f'bit{bit_index:02}_XOR2')
	carry_inner2 = label_gate(sum_inner, carry_in, 'AND', f'bit{bit_index:02}_AND2')
	
	assert(sum is not None)
	assert(carry_inner2 is not None)

	if sum != out:
		invalid_gates.add(sum)

	carry_out = label_gate(carry_inner1, carry_inner2, 'OR', f'bit{bit_index:02}_OR1')
	assert(carry_out is not None)

	return carry_out

outputs = find_gates('z')
bit_count = len(outputs)
carry_in = None
carry_out = f'z{bit_count:02}'

for bit_index in range(bit_count - 1):
	in_x = f'x{bit_index:02}'
	in_y = f'y{bit_index:02}'
	out_z = f'z{bit_index:02}'

	if bit_index == 0:
		carry_in = verify_half_adder(bit_index, in_x, in_y, out_z)
	else:
		carry_in = verify_full_adder(bit_index, in_x, in_y, carry_in, out_z)

	print(f'{bit_index:02}: s={out_z}; ci={carry_in}; co={carry_out}')

print(','.join(sorted(invalid_gates)))
