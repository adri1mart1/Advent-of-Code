import copy


max_col = max_row = 26


class Pos:

	def __init__(self, row, col, label=''):
		self.row = row
		self.col = col
		self.label = label


class Rope:
	def __init__(self, length):
		self.len = length
		self.knots = [Pos(0, 0, i) for i in range(self.len)]
		self.knots[0].label = 'H'
		self.tail_seen_pos = []
		self.copy_prev()

	def copy_prev(self):
		self.prev_knots = []
		for i in range(self.len):
			self.prev_knots.append(copy.deepcopy(self.knots[i]))

	def get(self, row, col):
		for i in range(self.len):
			if self.knots[i].row == row and self.knots[i].col == col:
				return self.knots[i]
		return None

	def print_m(self):
		print()
		for row in range(max_row):
			for col in range(max_col):
				p = self.get(row, col)
				if p:
					print(p.label, end='')
				else:
					print('.', end='')
			print()

	def check_seen_pos(self):
		t = (self.knots[-1].row, self.knots[-1].col)
		if t not in self.tail_seen_pos:
			self.tail_seen_pos.append(t)

	def knot_too_far(self, i):
		diff_r = self.knots[i-1].row - self.knots[i].row
		diff_c = self.knots[i-1].col - self.knots[i].col
		return abs(diff_r) > 1 or abs(diff_c) > 1

	def go(self, direction, val):
		move_row = 0
		move_col = 0

		if direction == 'up':
			move_row = -1
		elif direction == 'down':
			move_row = 1
		elif direction == 'right':
			move_col = 1
		elif direction == 'left':
			move_col = -1

		for v in range(val):
			self.knots[0].row += move_row
			self.knots[0].col += move_col

			for i in range(1, self.len):
				if self.knot_too_far(i):
					diff_r = self.knots[i-1].row - self.knots[i].row
					diff_c = self.knots[i-1].col - self.knots[i].col

					if diff_r >= 1:
						self.knots[i].row += 1
					elif diff_r <= -1:
						self.knots[i].row -= 1

					if diff_c >= 1:
						self.knots[i].col += 1
					elif diff_c <= -1:
						self.knots[i].col -= 1

			self.check_seen_pos()
			self.copy_prev()


if __name__ == "__main__":

	with open('in.txt') as file:
		data = [l.rstrip() for l in file]

	rope_p1 = Rope(2)
	rope_p2 = Rope(10)

	for d in data:
		val = int(d.split(' ')[1])
		# rope.print_m()

		if d[0] == 'R':
			rope_p1.go('right', val)
			rope_p2.go('right', val)
		elif d[0] == 'L':
			rope_p1.go('left', val)
			rope_p2.go('left', val)
		elif d[0] == 'U':
			rope_p1.go('up', val)
			rope_p2.go('up', val)
		elif d[0] == 'D':
			rope_p1.go('down', val)
			rope_p2.go('down', val)


	print("Part1: tail of rope length two explored {} tiles".format(len(rope_p1.tail_seen_pos)))
	print("Part2: tail of rope length two explored {} tiles".format(len(rope_p2.tail_seen_pos)))
