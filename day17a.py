import aoc, util
import numpy as np
import re

class CPU:
	def __init__(self, reg_a, reg_b, reg_c):
		self.reg_a = reg_a
		self.reg_b = reg_b
		self.reg_c = reg_c
		self.instruction_pointer = 0
		self.output = [ ]

		self.instructions = \
		[
			('ADV', self.adv, True),
			('BXL', self.bxl, False),
			('BST', self.bst, True),
			('JNZ', self.jnz, False),
			('BXC', self.bxc, False),
			('OUT', self.out, True),
			('BDV', self.bdv, True),
			('CDV', self.cdv, True),
		]

	def run(self, program):
		while self.instruction_pointer < len(program):
			opcode = program[self.instruction_pointer]
			operand = program[self.instruction_pointer + 1]

			self.instruction_pointer += 2

			instruction_label, instruction_func, is_combo_operand = self.instructions[opcode]

			if is_combo_operand:
				operand = self.combo_operand(operand)

			print(instruction_label, operand)

			instruction_func(operand)


	def disassemble(self, program):
		for ip in range(0, len(program), 2):
			opcode = program[ip]
			operand = program[ip + 1]

			instruction_label, instruction_func, is_combo_operand = self.instructions[opcode]

			if is_combo_operand and operand >= 4:
				operand = chr(ord('A') + (operand - 4))

			print(instruction_label, operand)


	def combo_operand(self, operand):
		if operand <= 3:
			return operand
		
		if operand == 4:
			return self.reg_a
		elif operand == 5:
			return self.reg_b
		elif operand == 6:
			return self.reg_c
		
		raise 'Invalid operand'
	
	def adv(self, operand):
		self.reg_a = self.reg_a // (2 ** operand)
	
	def bxl(self, operand):
		self.reg_b = self.reg_b ^ operand
	
	def bst(self, operand):
		self.reg_b = operand & 0x07
	
	def jnz(self, operand):
		if self.reg_a != 0:
			self.instruction_pointer = operand
	
	def bxc(self, operand):
		self.reg_b = self.reg_b ^ self.reg_c
	
	def out(self, operand):
		v = operand & 0x07

		self.output.append(v)
		print(f'Output: {v}')
	
	def bdv(self, operand):
		self.reg_b = self.reg_a // (2 ** operand)
	
	def cdv(self, operand):
		self.reg_c = self.reg_a // (2 ** operand)

input = aoc.load_input(mode=aoc.MODE_LINES)

reg_a = int(re.search('Register A: (\\d+)', input[0]).group(1))
reg_b = int(re.search('Register B: (\\d+)', input[1]).group(1))
reg_c = int(re.search('Register C: (\\d+)', input[2]).group(1))

program = list(map(int, re.search('Program: ((\\d,?)+)', input[4]).group(1).split(',')))

print(reg_a, reg_b, reg_c, program)

cpu = CPU(reg_a, reg_b, reg_c)
cpu.disassemble(program)

print('---')

cpu.run(program)

print('---')

result = ','.join(map(str, cpu.output))
print(result)