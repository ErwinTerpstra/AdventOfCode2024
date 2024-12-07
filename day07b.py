import aoc

input = aoc.load_input(
	mode=aoc.MODE_GRID, 
	dtype=int, 
	column_separator=' ',
	preprocess=lambda x: x.replace(':', ''))

def try_solve(test_value, operands, operand_index):
	rhs = operands[operand_index]

	if operand_index == 1:
		return test_value == rhs

	if test_value >= rhs:
		if try_solve(test_value - rhs, operands, operand_index - 1):
			return True

	if test_value % rhs == 0:
		if try_solve(test_value // rhs, operands, operand_index - 1):
			return True
		
	rhs_str = str(rhs)
	test_value_str = str(test_value)
	if test_value_str.endswith(rhs_str):
		if try_solve(int(test_value_str[:len(test_value_str) - len(rhs_str)]), operands, operand_index - 1):
			return True

	return False

is_line_valid = lambda values: try_solve(values[0], values, len(values) - 1)	
valid_test_values = [ values[0] for values in input if is_line_valid(values) ]

result = sum(valid_test_values)
print(result)