import collections

# Definitely not my best solve ! Most of the solutions I've compared online used
# set() to keep track of position and that's was way more efficient and smart.
# My implementation allocate a matrix, wide enough so there's no risk on being
# out of the bounds.
# Part2 is quite slow (about 1min to get the result) because of this.

y_max = 500
x_max = 500
offset = 200


adjacents = [
	(-1,-1), (-1,0, -1,1),
	(0,-1), (0,1),
	(1,-1), (1,0), (1,1)
]

def print_mat(m):
	for y in range(len(m)):
		for x in range(len(m[0])):
			print(m[y][x], end='')
		print()

def is_elf_N_NE_NW(m, x, y):
	return m[y-1][x-1] == '#' or m[y-1][x] == '#' or m[y-1][x+1] == '#'

def is_elf_S_SE_SW(m, x, y):
	return m[y+1][x-1] == '#' or m[y+1][x] == '#' or m[y+1][x+1] == '#'

def is_elf_W_NW_SW(m, x, y):
	return mat[y-1][x-1] == '#' or mat[y][x-1] == '#' or mat[y+1][x-1] == '#'

def is_elf_E_NE_SE(m, x, y):
	return mat[y-1][x+1] == '#' or mat[y][x+1] == '#' or mat[y+1][x+1] == '#'

def is_elf_arround(m, x, y):
	return is_elf_N_NE_NW(m,x,y) or \
	       is_elf_E_NE_SE(m,x,y) or \
	       is_elf_S_SE_SW(m,x,y) or \
	       is_elf_W_NW_SW(m,x,y)


mat = [['.' for i in range(x_max)] for _ in range(y_max)]

with open('in.txt') as file:
	data = [l.rstrip() for l in file]

for y in range(len(data)):
	for x in range(len(data[0])):
		mat[y+offset][x+offset] = data[y][x]

adjacents_order = collections.deque(['N','S','W','E'])


r = 1 # number of round

while True:

	# first half: check if elves need to move
	init_pos = []
	next_pos = []

	for y in range(len(mat)):
		for x in range(len(mat[0])):
			if mat[y][x] == '.':
				continue

			init_pos.append((x,y))

			if is_elf_arround(mat, x, y):
				move_found = False

				for adjo in adjacents_order:
					if adjo == 'N':
						if not is_elf_N_NE_NW(mat, x, y):
							next_pos.append((x,y-1))
							move_found = True
							break
					elif adjo == 'S':
						if not is_elf_S_SE_SW(mat, x, y):
							next_pos.append((x,y+1))
							move_found = True
							break
					elif adjo == 'E':
						if not is_elf_E_NE_SE(mat, x, y):
							next_pos.append((x+1,y))
							move_found = True
							break
					elif adjo == 'W':
						if not is_elf_W_NW_SW(mat, x, y):
							next_pos.append((x-1,y))
							move_found = True
							break
					else:
						assert False

				if not move_found:
					next_pos.append((x,y))

			else:
				# do not move
				next_pos.append((x,y))

	if init_pos == next_pos:
		print('Part2: At round {} no move from any elf'.format(r))
		break

	# second half: move elves
	while True:
		if len(init_pos) == 0:
			break

		ip = init_pos.pop(0) # initial position
		np = next_pos.pop(0) # next position

		if np in next_pos:
			while np in next_pos:
				idx = next_pos.index(np)
				init_pos.pop(idx)
				next_pos.pop(idx)

		else:
			mat[ip[1]][ip[0]] = '.'
			mat[np[1]][np[0]] = '#'

	if r == 10:
		elf_min_x = x_max
		elf_min_y = y_max
		elf_max_x = 0
		elf_max_y = 0

		for y in range(y_max):
			for x in range(x_max):
				if mat[y][x] == '#':
					elf_min_x = min(x, elf_min_x)
					elf_min_y = min(y, elf_min_y)
					elf_max_x = max(x, elf_max_x)
					elf_max_y = max(y, elf_max_y)

		empty_tiles = 0

		for y in range(elf_min_y, elf_max_y+1):
			for x in range(elf_min_x, elf_max_x+1):
				if mat[y][x] == '.':
					empty_tiles += 1

		print('Part1: After 10 round, the number of empty_tiles is {}'.format(empty_tiles))

	r += 1
	adjacents_order.rotate(-1)