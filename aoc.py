import sys
import numpy as np

from pathlib import Path

MODE_LINES = 'lines'
MODE_GRID = 'grid'

def load_input(mode: str, remove_newlines = True, use_np = False, dtype=str):
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
		lines = [ line.split() for line in lines]
		lines = [ [ dtype(x) for x in line ] for line in lines ]
	else:
		line = [ dtype(line) for line in lines ]

	if use_np:
		lines = np.array(lines)

	return lines