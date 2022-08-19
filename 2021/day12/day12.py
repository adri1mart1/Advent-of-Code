from collections import Counter

caves = dict()
possible_paths_v1 = []
possible_paths_v2 = []


class Cave:
	def __init__(self, name):
		self.name = name
		self.links = []
		self.is_small_cave = name.islower()

	def add_link(self, to):
		assert(to not in self.links)
		self.links.append(to)

	def can_be_explored_v1(self, prev_path):
		return not self.is_small_cave or self.name not in prev_path

	def can_be_explored_v2(self, prev_path):
		if self.name == "start":
			return False
		elif not self.is_small_cave:
			return True
		elif self.name not in prev_path:
			return True
		else:
			lower_prev_path = [x for x in prev_path if x.islower()]
			if any({k:v for (k,v) in dict(Counter(lower_prev_path)).items() if v > 1}):
				return False
		return True

	def explore_v1(self, l=[]):
		prev_path = list(l)
		prev_path.append(self.name)

		if self.name == "end":
			possible_paths_v1.append(prev_path)
		else:
			for link in self.links:
				if caves[link].can_be_explored_v1(prev_path):
					caves[link].explore_v1(prev_path)

	def explore_v2(self, l=[]):
		prev_path = list(l)
		prev_path.append(self.name)

		if self.name == "end":
			possible_paths_v2.append(prev_path)
		else:
			for link in self.links:
				if caves[link].can_be_explored_v2(prev_path):
					caves[link].explore_v2(prev_path)


class Map:
	def check_if_seen(self, fr):
		if fr not in caves:
			caves[fr] = Cave(fr)

	def add_link(self, fr, to):
		self.check_if_seen(fr)
		self.check_if_seen(to)
		caves[fr].add_link(to)
		caves[to].add_link(fr)

	def feed(self, l):
		self.add_link(l.split('-')[0], l.split('-')[1])

	def explore_v1(self):
		caves["start"].explore_v1()
		print("Part1: number of possible path: {}".format(len(possible_paths_v1)))

	def explore_v2(self):
		caves["start"].explore_v2()
		print("Part2: number of possible path: {}".format(len(possible_paths_v2)))


m = Map()

with open("in.txt") as f:
	for line in f:
		m.feed(line.rstrip())

m.explore_v1()
m.explore_v2()
