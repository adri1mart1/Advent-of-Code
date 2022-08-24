import copy

matrix = []
x_max = int
y_max = int


def print_mat(m):
	print("matrix:")
	for y in range(y_max):
		for x in range(x_max):
			print(m[y][x], end='')
		print()


def move(east=True):
	global matrix
	new_mat = copy.deepcopy(matrix)
	has_move = False

	for y in reversed(range(y_max)):
		for x in reversed(range(x_max)):
			nextx = (x+1) % x_max
			nexty = (y+1) % y_max
			if east:
				if matrix[y][x] == '>' and matrix[y][nextx] == '.':
					new_mat[y][x] = '.'
					new_mat[y][nextx] = '>'
					has_move = True
			else: # south
				if matrix[y][x] == 'v' and matrix[nexty][x] == '.':
					new_mat[y][x] = '.'
					new_mat[nexty][x] = 'v'
					has_move = True
	matrix = copy.deepcopy(new_mat)
	return has_move


def run():
	global matrix
	i = 1
	while True:
		res_e = move(east=True)
		res_s = move(east=False)
		# print_mat(matrix)

		if not res_e and not res_s:
			print("Part1: no move detected at step {}".format(i))
			break

		i += 1


with open("in.txt") as f:
	for line in f:
		matrix.append([c for c in line.rstrip()])

x_max, y_max = len(matrix[0]), len(matrix)

run()