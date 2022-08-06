from collections import Counter


digit_1 = 2
digit_4 = 4
digit_7 = 3
digit_8 = 7


class Solver:
	def __init__(self, line):
		self.expected_length = {
			0: 6,
			1: 2,
		    2: 5,
		    3: 5,
		    4: 4,
		    5: 5,
		    6: 6,
		    7: 3,
		    8: 7,
		    9: 6
		}
		self.whole_line = line
		self.input_table = line[:line.find('|')].split()
		self.output_line = line[line.find('|')+2:].split()
		self.number_to_str = dict()
		self.str_to_number = dict()

	def process_len(self, number):
		for e in self.input_table:
			if len(e) == self.expected_length[number]:
				self.number_to_str[number] = e
				self.str_to_number[e] = number
				self.input_table.remove(e)
				return
		assert(False)

	def get_count_common_letters(self, word, subword):
		r = Counter(word) & Counter(subword)
		return sum(r.values())

	def deduce_number(self, number, contained_num, but=0):
		for e in self.input_table:
			if  len(e) == self.expected_length[number] and \
			    self.get_count_common_letters(e, self.number_to_str[contained_num]) == len(self.number_to_str[contained_num])-but:

				self.number_to_str[number] = e
				self.str_to_number[e] = number
				self.input_table.remove(e)
				return
		assert(False)

	def process(self):
		self.process_len(1) # guess 1
		self.process_len(8) # guess 8
		self.process_len(7) # guess 7
		self.process_len(4) # guess 4
		self.deduce_number(3, 1) # guess 3
		self.deduce_number(2, 4, 2) # guess 2
		self.deduce_number(5, 4, 1) # guess 5
		self.deduce_number(6, 1, 1) # guess 6
		self.deduce_number(9, 4) # guess 9
		# 0 is the remaining one
		self.number_to_str[0] = self.input_table[0]
		self.str_to_number[self.input_table[0]] = 0

		return 1000 * self.find_num(self.output_line[0]) + 100 * self.find_num(self.output_line[1]) + \
		       10 * self.find_num(self.output_line[2]) + self.find_num(self.output_line[3])

	def find_num(self, word):
		for key, value in self.str_to_number.items():
			if all([c in word for c in key]) and len(key) == len(word):
				return value


with open("in.txt") as f:
	lines = [x.rstrip() for x in f.readlines()]
	counters = dict()
	for line in lines:
		counters = dict(Counter(counters) + Counter(map(len, line[line.find('|')+2:].split())))

print("part1: Number of 1,2,4,7: {}".format(counters[digit_1]+counters[digit_4]+counters[digit_7]+counters[digit_8]))


with open("in.txt") as f:
	lines = [x.rstrip() for x in f.readlines()]
	total = 0
	for line in lines:
		s = Solver(line)
		total += s.process()

print("part2: Total: {}".format(total))



