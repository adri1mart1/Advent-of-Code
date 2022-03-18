class Grids:

	def __init__(self):
		self.mat = [[0 for x in range(5)] for y in range(5)]
		self.check = [[0 for x in range(5)] for y in range(5)]
		self.win = False

	def feed(self, i, line):
		assert i >= 0
		assert i < 5
		self.mat[i] = [int(a) for a in line.split()]

	def print(self):
		for i in range(5):
			print(self.mat[i])
		print()

	def get_sum_unmarked(self) -> int:
		res = 0
		for i in range(5):
			for j in range(5):
				res += self.mat[i][j] if self.check[i][j] == 0 else 0
		return res

	def check_win(self) -> bool:
		for i in range(5):
			if (self.check[i][0] == 1 and \
			    self.check[i][1] == 1 and \
			    self.check[i][2] == 1 and \
			    self.check[i][3] == 1 and \
			    self.check[i][4] == 1) or \
			   (self.check[0][i] == 1 and \
			    self.check[1][i] == 1 and \
			    self.check[2][i] == 1 and \
			    self.check[3][i] == 1 and \
			    self.check[4][i] == 1):
			    self.win = True

	def set(self, n) -> int:
		for i in range(5):
			for j in range(5):
				if self.mat[i][j] == n:
					self.check[i][j] = 1

		self.check_win()

		if self.win:
			return self.get_sum_unmarked()
		return 0

# read inputs
with open("in.txt") as f:
	digits = [int(d) for d in f.readline().rstrip().split(',')]
	grids = [s.rstrip() for s in f.readlines() if s is not '\n']
assert len(grids)%5 == 0

# deduce number of grids
n_grids = int(len(grids)/5)

# fill a table with all grids
all_g = []
for i in range(n_grids):
	g = Grids()
	for j in range(5):
		g.feed(j, grids[5*i+j])
	all_g.append(g)

# loop for all digits.
# on each loop, we keep only grids that did not win yet
# we continue looping till all grids are resolved and
# print results
remaning_grids = all_g
first_win = True
for d in digits:
	tmp_g = []

	for g in remaning_grids:
		s = g.set(d)
		if s > 0:
			if first_win:
				print("part1: first win board score: {}".format(s*d))
				first_win = False
		else:
			tmp_g.append(g)

	if len(tmp_g) == 0:
		print("part2: last win board score: {}".format(remaning_grids[0].get_sum_unmarked() * d))
		exit(0)

	remaning_grids = tmp_g
