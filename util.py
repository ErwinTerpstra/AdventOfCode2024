import itertools
import math
from collections import defaultdict

in_grid = lambda pos, size: pos[0] >= 0 and pos[1] >= 0 and pos[0] < size[1] and pos[1] < size[1]
all_coordinates = lambda size, padding=0: itertools.product(*( range(padding, dim - padding) for dim in size ))
filter_none = lambda items: (x for x in items if x is not None)

def min_item(items, key=lambda x: x):
	lowest_item = None
	lowest_val = None

	for item in items:
		value = key(item)
		if lowest_val is None or value < lowest_val:
			lowest_item = item
			lowest_val = value

	return lowest_item

def max_item(items, key=lambda x: x):
	highest_item = None
	highest_val = None

	for item in items:
		value = key(item)
		if highest_val is None or value > highest_val:
			highest_item = item
			highest_val = value

	return highest_item

def max_safe(*args):
	c = sum(1 for x in filter_none(args))

	if c == 0:
		return None
	
	if c == 1:
		return next(filter_none(args))

	return max(*filter_none(args))

def min_safe(*args):
	c = sum(1 for x in filter_none(args))

	if c == 0:
		return None
	
	if c == 1:
		return next(filter_none(args))

	return min(*filter_none(args))

def argmin(items, key=lambda x: x):
	lowest_i = None
	lowest_val = None

	for i in range(len(items)):
		value = key(items[i])
		if lowest_val is None or value < lowest_val:
			lowest_i = i
			lowest_val = value

	return lowest_i

def expand_args(lhs, rhs):
	l_is_iter = is_iterable(lhs)
	r_is_iter = is_iterable(rhs)

	if l_is_iter is not r_is_iter:
		size = len(lhs) if l_is_iter else len(rhs)

	lhs = lhs if l_is_iter else [ lhs ] * size
	rhs = rhs if r_is_iter else [ rhs ] * size

	return lhs, rhs

def is_iterable(item) -> bool:
	try:
		iterator = iter(item)
	except TypeError:
		return False
	else:
		return True

def pairs_to_dict(items):
	"""Creates dictionary from list of key-value pairs.  E.g.: [ (key1, value1), (key2, value2), (key3, value3) ]"""
	d = defaultdict(list)
	
	for item in items:
		d[item[0]].append(item[1])

	return d

def reversed_as_tuple(iter):
	"""Reverse the given iterator, return as tuple"""
	return tuple(reversed(tuple(iter)))

def groupby(items, key):
	"""Group the given items by a key. Returns a dictionary of lists"""
	d = defaultdict(list)

	for item in items:
		d[key(item)].append(item)

	return d

def first_index(items, predicate):
	iter = (i for i, v in enumerate(items) if predicate(v))
	return next(iter, -1)

def index(items, value, key=lambda x: x):
	iter = (i for i, v in enumerate(items) if key(v) == value)
	return next(iter, -1)

class Point(tuple):

	rotCW = lambda self: Point((self[1], -self[0]))
	rotCCW = lambda self: Point((-self[1], self[0]))

	__add__ = lambda self, other: add(self, other)
	__sub__ = lambda self, other: sub(self, other)
	__mul__ = lambda self, other: mul(self, other)
	__floordiv__ = lambda self, other: div(self, other)
	__mod__ = lambda self, other: mod(self, other)
	__abs__ = lambda self: Point((abs(x) for x in self))

# General arithmetic operators for multidimensional tuples
add = lambda lhs, rhs: Point((a + b for a, b in zip(*expand_args(lhs, rhs))))
sub = lambda lhs, rhs: Point((a - b for a, b in zip(*expand_args(lhs, rhs))))
mul = lambda lhs, rhs: Point((a * b for a, b in zip(*expand_args(lhs, rhs))))
div = lambda lhs, rhs: Point((a // b for a, b in zip(*expand_args(lhs, rhs))))
mod = lambda lhs, rhs: Point((a % b for a, b in zip(*expand_args(lhs, rhs))))
neg = lambda value: Point((-x for x in value))

sign = lambda value: math.copysign(1, value)

# Grid utils
ZERO = Point((0, 0))
ONE = Point((1, 1))

LEFT = Point((0, -1))
RIGHT = Point((0, 1))
UP = Point((-1, 0))
DOWN = Point((1, 0))

CARDINAL_DIRECTIONS = \
[
	LEFT, RIGHT, UP, DOWN
]