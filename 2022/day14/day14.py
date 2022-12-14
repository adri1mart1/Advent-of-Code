import os
import time
from bresenham import bresenham

# just for the fun of it :) (not really suitable for main input)
print_part1 = False

# example
# x_max = 550
# y_max = 12

# main
x_max = 1000
y_max = 200

mat = [['.' for y in range(y_max)] for x in range(x_max)]
start = (500, 0)
mat[start[0]][start[1]] = 's'


def print_mat():
	for y in range(0, y_max):
		for x in range(450, x_max):
			print(mat[x][y], end='')
		print()


def pour_sand(p):
	pos = p

	# check down
	if p[1]+1 >= y_max:
		raise ValueError()

	if mat[p[0]][p[1]+1] == '.':
		pos = pour_sand((p[0], p[1]+1))

	# check left
	elif mat[p[0]-1][p[1]+1] == '.':
		pos = pour_sand((p[0]-1, p[1]+1))

	# check right
	elif mat[p[0]+1][p[1]+1] == '.':
		pos = pour_sand((p[0]+1, p[1]+1))

	return pos


with open('in.txt') as file:
	data = [l.rstrip() for l in file]

lines = []

for d in data:
	points = d.split(' -> ')
	for i in range(len(points)-1):
		p1 = int(points[i].split(',')[0])
		p2 = int(points[i].split(',')[1])
		p3 = int(points[i+1].split(',')[0])
		p4 = int(points[i+1].split(',')[1])
		lines.append(((p1,p2),(p3,p4)))

for line in lines:
	# use of bresenham algorithm to find all coordinates in between 2 points
	points = list(bresenham(line[0][0], line[0][1], line[1][0], line[1][1]))

	for point in points:
		mat[point[0]][point[1]] = '#'


# start pouring sand
sand = 0

while True:
	sand += 1

	if print_part1:
		os.system('clear')
		print_mat()
		time.sleep(.1)

	try:
		pos = pour_sand(start)
	except ValueError:
		print('Part1: detected flowing with {} sand unit'.format(sand-1))
		break

	mat[pos[0]][pos[1]] = 'o'


# reset sand for part 2 and find lowest rock
max_y = 0
for y in range(0, y_max):
	for x in range(0, x_max):
		if mat[x][y] == 'o':
			mat[x][y] = '.'
		if mat[x][y] == '#':
			max_y = max(max_y, y)
max_y += 2


# add floor
for x in range(x_max):
	mat[x][max_y] = '#'


# start pouring sand again
sand = 0

while True:
	sand += 1

	pos = pour_sand(start)

	if pos == start:
		print('Part2: with floor, detected flowing with {} sand unit'.format(sand))
		break

	mat[pos[0]][pos[1]] = 'o'
