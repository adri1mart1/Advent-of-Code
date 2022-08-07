x_len = 100
y_len = 100

mat = [[0 for y in range(y_len)] for x in range(x_len)]
low_points = []
points_to_check = []
points_checked = []
all_bassins = []


class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def print(self):
		print("Point [{};{}]".format(self.x, self.y))

	def str(self):
		return "[{};{}]".format(self.x, self.y)

	def __eq__(self, p):
		return self.x == p.x and self.y == p.y

	def value(self):
		return mat[self.x][self.y]


def print_mat():
	for y in range(y_len):
		for x in range(x_len):
			print(mat[x][y], end='')
		print()


def is_valid_neighour(p):
	return p.x >= 0 and p.x < x_len and p.y >= 0 and p.y < y_len


def is_valid_bassin(p_to_check, p_from):
	if  is_valid_neighour(p_to_check) and \
	    p_to_check not in points_checked and \
	    p_to_check not in points_to_check and \
	    p_to_check.value() > p_from.value() and \
	    p_to_check.value() != 9:
	    return True
	return False


with open("in.txt") as f:
	for y in range(0, y_len):
		x = 0
		for c in f.readline().rstrip():
			mat[x][y] = int(c)
			x += 1


risk_level = 0
for x in range(x_len):
	for y in range(y_len):
		if  (x == 0 or (x > 0 and mat[x-1][y] > mat[x][y])) and \
			(y == 0 or (y > 0 and mat[x][y-1] > mat[x][y])) and \
			(x == x_len-1 or (x < x_len-1 and mat[x+1][y] > mat[x][y])) and \
			(y == y_len-1 or (y < y_len-1 and mat[x][y+1] > mat[x][y])):

				risk_level += 1+mat[x][y]
				low_points.append(Point(x, y))

print("part1: risk level: {}".format(risk_level))


for lp in low_points:
	points_to_check = []
	points_checked = []
	points_to_check.append(lp)

	for p in points_to_check:
		points_checked.append(p)

		# check left
		pleft = Point(p.x-1, p.y)
		if is_valid_bassin(pleft, p):
			points_to_check.append(pleft)

		# check right
		pright = Point(p.x+1, p.y)
		if is_valid_bassin(pright, p):
			points_to_check.append(pright)

		# check top
		ptop = Point(p.x, p.y-1)
		if is_valid_bassin(ptop, p):
			points_to_check.append(ptop)

		# check bottom
		pbottom = Point(p.x, p.y+1)
		if is_valid_bassin(pbottom, p):
			points_to_check.append(pbottom)

	all_bassins.append(len(points_checked))


res = 1
for x in sorted(all_bassins)[-3:]:
	res *= x

print("part2: multiplication of 3 largest bassins: {}".format(res))