import sys

from pathlib import Path

MODE_LINES = 'lines'

def load_input(mode: str, remove_newlines = True):
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

	# mode == lines or others	
	return lines