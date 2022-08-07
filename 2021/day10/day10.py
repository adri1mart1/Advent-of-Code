
couples = {
	'[': ']',
	'{': '}',
	'(': ')',
	'<': '>'
}

def next(line):
	scores = {
		')': 3,
		']': 57,
		'}': 1197,
		'>': 25137
	}
	s = []
	for c in line:
		if c in couples:
			s.append(c)
		else:
			n = s.pop()
			if couples[n] != c:
				return scores[c]
	return 0


def compute(l):
	res = 0
	v = {
		')': 1,
		']': 2,
		'}': 3,
		'>': 4
	}
	for i in range(len(l)):
		res *= 5
		res += v[l[i]]
	return res


def fix(line):
	scores = {
		')': 3,
		']': 57,
		'}': 1197,
		'>': 25137
	}
	s = []
	for c in line:
		if c in couples:
			s.append(c)
		else:
			n = s.pop()
			if couples[n] != c:
				return
	end = []
	while len(s):
		end.append(couples[s.pop()])
	return compute(end)

with open("in.txt") as f:
	lines = [x.rstrip() for x in f.readlines()]
	score = 0
	scores = []
	for line in lines:
		score += next(line)

		res = fix(line)
		if res:
			scores.append(res)

scores.sort()
print("part1: number of points: {}".format(score))
print("part2: middle score: {}".format(scores[len(scores)//2]))
