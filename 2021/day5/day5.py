import math
from bresenham import bresenham

class Point:

	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

	def str(self):
		return "[{};{}]".format(self.x, self.y)


class Vent:

	def __init__(self, row):
		c1 = row[0].split(',')
		c2 = row[2].split(',')
		self.p1 = Point(int(c1[0]), int(c1[1]))
		self.p2 = Point(int(c2[0]), int(c2[1]))

	def print(self):
		print("p1: {} p2: {}".format(self.p1.str(), self.p2.str()))

	def horiz_or_vert(self):
		return True if self.p1.x == self.p2.x or self.p1.y == self.p2.y else False

	def get_all_points(self) -> []:
		# use of bresenham algorithm to find all coordinates in between 2 points
		rt = list(bresenham(self.p1.x, self.p1.y, self.p2.x, self.p2.y))
		res = []
		for r in rt:
			res.append(Point(r[0], r[1]))
		return res


class Diagram:

	def __init__(self):
		self.max_size = 1000
		# only horizontal and vert map
		self.hv_map  = [[0 for x in range(self.max_size)] for y in range(self.max_size)]
		# map with diagonals
		self.all_map = [[0 for x in range(self.max_size)] for y in range(self.max_size)]

	def print(self):
		print("horizontal and vert. map")
		for i in range(self.max_size):
			print(self.hv_map[i])
		print("\nwith diag. map")
		for i in range(self.max_size):
			print(self.all_map[i])
		print()

	def set(self, v):
		for p in v.get_all_points():
			if v.horiz_or_vert():
				self.hv_map[p.y][p.x] += 1
			self.all_map[p.y][p.x] += 1

	def count_overlap(self, only_horizon_and_vert=True):
		res = 0
		m = self.hv_map if only_horizon_and_vert else self.all_map
		for i in range(self.max_size):
			for j in range(self.max_size):
				if m[i][j] >= 2:
					res += 1
		return res


vents = []
with open("in.txt") as f:
	for line in f.readlines():
		vents.append(Vent(line.rstrip().split()))

d = Diagram()

for v in vents:
	d.set(v)

print("part1: overlap number: {}".format(d.count_overlap(only_horizon_and_vert=True)))
print("part2: overlap number: {}".format(d.count_overlap(only_horizon_and_vert=False)))

