import aoc, util
import re

import matplotlib.pyplot as plt
import numpy as np

from matplotlib.widgets import Slider

input = aoc.load_input(mode=aoc.MODE_LINES, remove_empty=True)
map_size = (11, 7) if aoc.input_type() == 'example' else (101, 103)

# Parse robots
robots = [ ]
for line in input:
	match = re.match('p=(\\-?\\d+),(\\-?\\d+) v=(\\-?\\d+),(\\-?\\d+)', line)

	p = (int(match[1]), int(match[2]))
	v = (int(match[3]), int(match[4]))

	robots.append((p, v))

# The function to be called anytime a slider's value changes
def update(value):
	t = 55 + value * map_size[0]

	img.fill(0)
	for p, v in robots:
		p_prime = util.mod(util.add(p, util.mul(v, t)), map_size)
		img[p_prime] += 1
		
	max = img.max()

	drawer.set_data(img.T)
	drawer.set_clim(vmax=max)

	fig.canvas.draw_idle()
	print(f'Showing iteration t={t}')

TOTAL_STEPS = 100

img = np.zeros(map_size, dtype=np.uint8)
fig, ax = plt.subplots()
drawer = ax.imshow(img.T, cmap='gray', vmin=0, vmax=255)
ax.set_xlabel('Time [s]')

# adjust the main plot to make room for the sliders
fig.subplots_adjust(left=0.25, bottom=0.25)

# Make a horizontal slider to control the frequency.
axfreq = fig.add_axes([0.25, 0.1, 0.65, 0.03])
time_slider = Slider(
	ax=axfreq,
	label='Time [s]',
	valmin=0,
	valmax=TOTAL_STEPS,
	valinit=0,
	valstep=1
)

time_slider.on_changed(update)

plt.show()
