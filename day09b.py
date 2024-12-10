import aoc, util
import itertools

create_map = lambda blocks: itertools.chain(*[ [ b['id'] ] * b['size'] for b in blocks ])

input = aoc.load_input(mode=aoc.MODE_GRID, use_numpy=False, dtype=int, column_separator='')[0]

blocks = [ ]
for i, size in enumerate(input):
	blocks.append({ 'id': i // 2 if i % 2 == 0 else -1, 'size': size })

max_fid = max(blocks, key=lambda x: x['id'])['id']

for fid in range(max_fid, -1, -1):
	file_idx = util.index(blocks, fid, key=lambda x: x['id'])
	file = blocks[file_idx]

	for target_idx in range(file_idx):
		target_block = blocks[target_idx]

		# Check if empty space of required size
		if target_block['id'] == -1 and target_block['size'] >= file['size']:
			file = blocks.pop(file_idx)

			# Update size of empty block, remove if zero
			target_block['size'] -= file['size']
			if target_block['size'] == 0:
				blocks.pop(target_idx)
			else:
				file_idx += 1

			# Insert the file block
			blocks.insert(target_idx, file)

			# Free up the space from moving the file
			prev_block = blocks[file_idx - 1]
			next_block = blocks[file_idx] if file_idx < len(blocks) else None
			if prev_block['id'] == -1:
				# Add freed up space to previous free block
				prev_block['size'] += file['size']

				# Merge if consecutive empty blocks
				if next_block is not None and next_block['id'] == -1:
					prev_block['size'] += next_block['size']
					blocks.pop(file_idx)
			elif next_block is not None and next_block['id'] == -1:
				# Add freed up space to next free block
				next_block['size'] += file['size']
			else:
				# Insert an empty block at old position
				blocks.insert(file_idx, { 'id': -1, 'size': file['size'] })

			break

	#print(list(create_map(blocks)))

result = sum((i * id for i, id in enumerate(create_map(blocks)) if id >= 0))

print(result)