x_max = 10
y_max = x_max
invalid = '-'


class Octopus:
	def __init__(self, x, y, e=invalid):
		self.x = x
		self.y = y
		self.energy = e
		self.reset()

	def reset(self):
		self.flash = False
		self.treated = False

	def increase(self):
		if self.energy == invalid or self.flash:
			return

		self.energy += 1
		if self.energy > 9:
			self.flash = True
			self.energy = 0

	def just_flashed(self) -> bool:
		if not self.treated and self.flash:
			self.treated = True
			return True
		return False

	def has_flashed(self) -> bool:
		return self.flash


class Map:
	def __init__(self):
		# allocate matrix with extra border to avoid dealing with out-of-bound indexes
		self.map = [[None for x in range(x_max+2)] for y in range(y_max+2)]
		# feed with invalid Octopus
		for y in range(0, y_max+2):
			for x in range(0, x_max+2):
				self.map[x][y] = Octopus(x, y)

		self.feed_y_index = 1
		self.iter = 0
		self.n_flash = 0
		self.full_flash = True

	def print(self):
		print("************")
		for y in range(0, y_max+2):
			for x in range(0, x_max+2):
				print("{}".format(self.map[x][y].energy), end='')
			print()
		print("************")

	def feed(self, line):
		assert(len(line) == x_max)
		x = 1
		for d in line:
			self.map[x][self.feed_y_index] = Octopus(x, self.feed_y_index, int(d))
			x += 1
		self.feed_y_index += 1

	def reset(self):
		self.full_flash = True
		for y in range(1, y_max+1):
			for x in range(1, x_max+1):
				self.map[x][y].reset()

	def step(self):
		# print("step {}".format(self.iter))
		self.reset()
		# self.print()

		# STEP 1: increase all octopus
		for y in range(1, y_max+1):
			for x in range(1, x_max+1):
				self.map[x][y].increase()

		# STEP 2: iterate over all octopus till we have treated all flashes
		more_flash_to_deal_with = True
		while more_flash_to_deal_with:
			more_flash_to_deal_with = False

			for y in range(1, y_max+1):
				for x in range(1, x_max+1):

					if self.map[x][y].just_flashed():
						self.map[x-1][y-1].increase()
						self.map[x-1][y].increase()
						self.map[x-1][y+1].increase()
						self.map[x][y-1].increase()
						self.map[x][y+1].increase()
						self.map[x+1][y-1].increase()
						self.map[x+1][y].increase()
						self.map[x+1][y+1].increase()

						more_flash_to_deal_with = True

		# STEP 3: count and detect full flash map
		for y in range(1, y_max+1):
			for x in range(1, x_max+1):
				if self.map[x][y].has_flashed():
					self.n_flash += 1
				else:
					self.full_flash = False

		self.iter += 1


m = Map()

with open("in.txt") as f:
	lines = [x.rstrip() for x in f.readlines()]

for line in lines:
	m.feed(line)


i = 1
while True:
	m.step()
	if i == 100:
		print("part1: number of flashes after 100 steps: {}".format(m.n_flash))

	if m.full_flash:
		print("part2: all Octopus have flashed at step {}".format(i))
		break

	i += 1