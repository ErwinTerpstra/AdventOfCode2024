import aoc, util
import numpy as np

input = aoc.load_input(mode=aoc.MODE_LINES)

NUMERIC_KEYPAD = np.array([
		[ '7', '8', '9' ],
		[ '4', '5', '6' ],
		[ '1', '2', '3' ],
		[ ' ', '0', 'A' ],
	])

DIRECTIONAL_KEYPAD = np.array([
		[ ' ', '^', 'A' ],
		[ '<', 'v', '>' ],
	])

KEYPADS = \
[
	NUMERIC_KEYPAD,
	DIRECTIONAL_KEYPAD,
	DIRECTIONAL_KEYPAD
]

DIR_CHARS = \
{
	util.UP: '^',
	util.DOWN: 'v',
	util.LEFT: '<',
	util.RIGHT: '>',
	util.ZERO: 'A'
}

CHAR_DIRS = { value: key for key, value in DIR_CHARS.items() }
CHAR_DIRS['A'] = util.ZERO

robot_positions = [ ]

for keypad in KEYPADS:
	robot_positions.append(util.first_position(keypad == 'A'))

def logio(func):
	def logger(*args, **kwargs):
		character = args[0]
		robot_idx = args[1] if len(args) > 1 else 0

		padding = '\t' * robot_idx

		print(f'{padding}Robot {robot_idx} - {character}; from {KEYPADS[robot_idx][robot_positions[robot_idx]]};')

		result = func(*args, **kwargs)

		if robot_idx == len(robot_positions) - 1:
			print(f'{padding}\tHuman: {"".join(result)} ({len(result)})')
		else:
			print(f'{padding}\tTotal: {len(result)}')

		return result

	return logger

#@logio
def press_keypad(character, robot_index = 0):
	keypad = KEYPADS[robot_index]
	position = robot_positions[robot_index]

	target = util.first_position(keypad == character)
	forbidden = util.first_position(keypad == ' ')

	delta = target - position

	vertical_sign = util.sign(delta[0])
	vertical_amount = abs(delta[0])

	horizontal_sign = util.sign(delta[1])
	horizontal_amount = abs(delta[1])

	vertical_actions = [ util.Point((vertical_sign, 0)) ] * vertical_amount
	horizontal_actions = [ util.Point((0, horizontal_sign)) ] * horizontal_amount
	v_first = [ *vertical_actions, *horizontal_actions, util.ZERO ]
	h_first = [ *horizontal_actions, *vertical_actions, util.ZERO ]

	# Move robot to target for next actions
	robot_positions[robot_index] = target
	
	# Last robot we enter the actions directly
	if robot_index >= len(KEYPADS) - 1:
		return [ DIR_CHARS[dir] for dir in v_first ]

	possible_paths = [ h_first, v_first ]
	allowed_paths = [ ]

	for path in possible_paths:
		pos = position
		crosses_forbidden = False

		for dir in path:
			pos += dir

			if pos == forbidden:
				crosses_forbidden = True
				break

		if crosses_forbidden: 
			continue

		allowed_paths.append(path)

	# Other robots have actions entered by even more robots
	best_result = None
	for path in allowed_paths:
		result = [ ]
		for dir in path:
			result.extend(press_keypad(DIR_CHARS[dir], robot_index + 1))

		if best_result is None or len(result) < len(best_result):
			best_result = result

	if best_result is None:
		raise 'Huh?'

	return best_result

result = 0
for code in input:
	actions = [ ]

	for character in code:
		path = press_keypad(character)
		actions.extend(path)

	result += int(code[0:-1]) * len(actions)

	print(f'{code} ({len(actions)}): {"".join(actions)}')

print(result)