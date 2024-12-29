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
 	*[ DIRECTIONAL_KEYPAD ] * 25,
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

cache = { }

def press_keypad(character, robot_index = 0):
	keypad = KEYPADS[robot_index]
	position = robot_positions[robot_index]

	target = util.first_position(keypad == character)
	
	# Move robot to target for next actions
	robot_positions[robot_index] = target

	# Check if we already cached this result
	cache_key = (robot_index, position, target)
	if cache_key in cache:
		return cache[cache_key]

	forbidden = util.first_position(keypad == ' ')
	delta = target - position

	vertical_sign = util.sign(delta[0])
	vertical_amount = abs(delta[0])

	horizontal_sign = util.sign(delta[1])
	horizontal_amount = abs(delta[1])

	# Last robot we enter the actions directly
	if robot_index >= len(KEYPADS) - 1:
		result = vertical_amount + horizontal_amount + 1
		cache[cache_key] = result

		return result

	vertical_actions = [ util.Point((vertical_sign, 0)) ] * vertical_amount
	horizontal_actions = [ util.Point((0, horizontal_sign)) ] * horizontal_amount
	
	if target[0] == forbidden[0] and position[1] == forbidden[1]:
		v_first = False
	elif target[1] == forbidden[1] and position[0] == forbidden[0]:
		v_first = True
	else:
		v_first = horizontal_sign != -1

	if v_first:
		a1 = vertical_actions
		a2 = horizontal_actions
	else:
		a1 = horizontal_actions
		a2 = vertical_actions

	result = 0
	for dir in (*a1, *a2, util.ZERO):
		result += press_keypad(DIR_CHARS[dir], robot_index + 1)

	cache[cache_key] = result

	return result

result = 0
for code in input:
	action_count = 0

	for character in code:
		action_count += press_keypad(character)

	result += int(code[0:-1]) * action_count

	print(f'{code}: {action_count}')

print(result)