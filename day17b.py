import aoc, util
import numpy as np
import itertools as it
import re

INSTRUCTIONS = \
[
	('ADV', lambda operand: f'reg_a = reg_a >> {operand}', True),
	('BXL', lambda operand: f'reg_b = reg_b ^ {operand}', False),
	('BST', lambda operand: f'reg_b = {operand} & 0x07', True),
	('JNZ', lambda operand: f'', False),
	('BXC', lambda operand: f'reg_b = reg_b ^ reg_c', False),
	('OUT', lambda operand: f'out = {operand} & 0x07 ', True),
	('BDV', lambda operand: f'reg_b = reg_a >> {operand}', True),
	('CDV', lambda operand: f'reg_c = reg_a >> {operand}', True),
]

def find_input_bits(input, output):
	start = 1 if input == 0 else 0
	for i in range(start, 8):
		reg_a, out = program_pass(input | i)
		if out == output:
			yield i
	
def reverse_program(program, input = None, end = None):
	end = end if end is not None else len(program) - 1
	input = input if input is not None else 0

	input = input << 3
	output = program[end]

	for possible_bits in find_input_bits(input, output):
		new_input = input | possible_bits
		if end > 0:
			result = reverse_program(program, new_input, end - 1)

			if result is not None:
				return result
		else:
			return new_input

	# No solution found
	return None

	for output in reversed(program):
		input = input << 3

		#print(f'Finding {output} ({output:03b}) with input {input} ({input:b})')
		possible_bits = find_input_bits(input, output)

		#print(f'Found {bits} ({bits:03b})')
		input |= bits

	return input

def exec_recompiled(reg_a_init):
	reg_a = reg_a_init
	output = [ ]

	while reg_a != 0:
		reg_a, out = program_pass(reg_a)
		output.append(out)

	return output

def recompile(program):
	output = 'def program_pass(reg_a):\n'
	output += '    reg_b = 0\n'
	output += '    reg_c = 0\n'
	output += '    \n'

	for opcode, operand in zip(program[::2], program[1::2]):
		op_label, op_func, op_combo = INSTRUCTIONS[opcode]

		if op_combo and operand >= 4:
			operand = f'reg_{chr(ord("a") + (operand - 4))}'

		output += f'    {op_func(operand)}\n'

	output += '    return reg_a, out'

	print('---')
	print(output)
	print('---')

	exec(output, globals())

input = aoc.load_input(mode=aoc.MODE_LINES)

program = list(map(int, re.search('Program: ((\\d,?)+)', input[4]).group(1).split(',')))
print(f'Program: {program}')

recompile(program)
input = reverse_program(program)
print(f'Found input: {input}')

output = exec_recompiled(input)
print(f'Output: {output}')