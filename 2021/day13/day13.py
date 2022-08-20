max_x = 0
max_y = 0
part1_answer = 0


class Coordinates:
	def __init__(self, line):
		global max_x, max_y
		self.x = int(line.split(',')[0])
		self.y = int(line.split(',')[1])
		if self.x > max_x:
			max_x = self.x
		if self.y > max_y:
			max_y = self.y

	def __hash__(self):
		return hash((self.x, self.y))

	def __eq__(self, c):
		if not isinstance(c, type(self)):
			return NotImplemented
		return self.x == c.x and self.y == c.y


class FoldInstruction:
	def __init__(self, line):
		self.along = line.split(' ')[2].split('=')[0]
		self.value = int(line.split(' ')[2].split('=')[1])

	def adjust_map_size(self):
		global max_x, max_y
		if self.along == 'y':
			max_y = int(max_y/2)
		else:
			max_x = int(max_x/2)

	def transform(self, c):
		if self.along == 'y' and c.y > self.value:
				c.y -= 2*(c.y - self.value)
		if self.along == 'x':
			if c.x > self.value:
				diff = c.x - self.value
				c.x -= 2*diff


def print_map(coords):
	global max_x, max_y
	m = [['.' for x in range(max_y)] for y in range(max_x)]

	for c in coordinates:
		m[c.x][c.y] = '#'

	for y in range(max_y):
		for x in range(max_x):
			print(m[x][y], end='')
		print()


coordinates = []
fold_instructions = []

with open("in.txt") as f:
	for line in f:
		if line[0].isdigit():
			coordinates.append(Coordinates(line.rstrip()))
		elif line[0] == 'f':
			fold_instructions.append(FoldInstruction(line.rstrip()))


for fi in fold_instructions:
	fi.adjust_map_size()

	for c in coordinates:
		fi.transform(c)

	coordinates = list(set(coordinates))

	if part1_answer == 0:
		part1_answer = len(coordinates)

print("Part1: Number of dots after folding once: {}".format(part1_answer))
print("Part2: Secret password")
print_map(coordinates)