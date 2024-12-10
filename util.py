
from collections import defaultdict

# General arithmetic operators for multidimensional tuples
add = lambda lhs, rhs: tuple((a + b for a, b in zip(*expand_args(lhs, rhs))))
sub = lambda lhs, rhs: tuple((a - b for a, b in zip(*expand_args(lhs, rhs))))
mul = lambda lhs, rhs: tuple((a * b for a, b in zip(*expand_args(lhs, rhs))))
div = lambda lhs, rhs: tuple((a // b for a, b in zip(*expand_args(lhs, rhs))))

neg = lambda value: tuple((-x for x in value))

in_grid = lambda pos, size: pos[0] >= 0 and pos[1] >= 0 and pos[0] < size[1] and pos[1] < size[1]

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

def index(items, value, key=lambda x: x):
	iter = (i for i, v in enumerate(items) if key(v) == value)
	return next(iter)