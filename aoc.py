import sys
import numpy as np

from pathlib import Path

MODE_LINES = 'lines'
MODE_GRID = 'grid'
MODE_STRING = 'string'

def load_input(
		mode: str, 
		remove_newlines = True, 
		column_separator = None,
		use_numpy = False, 
		dtype=str, 
		numpy_axis = 0):
	"""Load input based on the current executing script."""

	# Determine input type from command line parameters
	# Should usually be 'input' or 'example'
	input_type = sys.argv[1] if len(sys.argv) >= 2 else 'input'

	# Get the name of the executing script file
	script_file = Path(sys.argv[0])

	# Remove "part a/b" suffix
	day_name = script_file.stem
	if day_name.endswith(('a', 'b')):
		day_name = day_name[0:-1]

	# Determine input file name based on script file + input type
	input_file = f'{day_name}_{input_type}.txt'

	# Read the input file
	with open(input_file) as f:
		lines = f.readlines()

	# Remove newlines if desired
	if remove_newlines:
		lines = [ line.replace('\r', '').replace('\n', '') for line in lines ]

	# Split by whitespace into grid
	if mode == MODE_GRID:
		def split_line(line):
			return line.split(column_separator) if column_separator != '' else line
	
		lines = [ [ dtype(x) for x in split_line(line) ] for line in lines]
	elif mode == MODE_STRING:
		lines = ''.join(lines)
	else:
		lines = [ dtype(line) for line in lines ]

	# Convert to numpy
	if use_numpy:
		if numpy_axis == 1:
			lines = [ np.array(line) for line in lines ]
		else:
			lines = np.array(lines)

	# Random newline print since the debugger output starts on the same
	# line as the command line :/
	print('')

	return lines