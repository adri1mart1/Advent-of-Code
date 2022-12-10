
with open('in.txt') as file:
	data = [l.rstrip() for l in file]

cycle = 0
x = 1
strength = 0
index = 0
draw_line = []
sprite = list('###.....................................')
sprite_pos = 1

def move_sprite(pos):
	global sprite, sprite_pos
	for i in range(3):
		idx = sprite_pos+i-1
		if idx >= 0 and idx < len(sprite):
			sprite[idx] = '.'
	for i in range(3):
		idx = pos+i-1
		if idx >= 0 and idx < len(sprite):
			sprite[idx] = '#'
	sprite_pos = pos

def draw():
	global draw_line
	draw_line.append(sprite[(cycle % 40) -1])
	if (cycle % 40) == 0:
		print('Part2: {}'.format(''.join([c for c in draw_line])))
		draw_line = []

def next_cycle():
	global cycle, strength
	cycle += 1
	draw()
	if cycle >= 20 and (cycle - 20) % 40 == 0:
		strength += cycle * x


while True:

	if 'addx' in data[index]:
		next_cycle()
		next_cycle()
		x += int(data[index].split(' ')[1])
		move_sprite(x)

	elif 'noop' in data[index]:
		next_cycle()

	index += 1

	if index >= len(data):
		break

print('Part1: sum of the 6 signal strength {}'.format(strength))