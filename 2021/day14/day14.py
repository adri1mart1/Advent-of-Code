from collections import Counter

mapping = dict()
letter_cnt = dict()


def increase_letter_by(letter, by):
	global letter_cnt
	if letter in letter_cnt:
		letter_cnt[letter] += by
	else:
		letter_cnt[letter] = by


def init_dict(mainw):
	global letter_cnt
	letter_cnt = Counter(mainw)
	cnt = dict()
	for d in mapping:
		cnt[d] = 0
	for i in range(len(mainw)-1):
		word = mainw[i:i+2]
		cnt[word] += 1
	return cnt


def step(d: dict()):
	init_d = dict(d) # deep copy
	for k,v in init_d.items():
		if v == 0:
			continue
		inc1 = k[0] + mapping[k]
		inc2 = mapping[k] + k[1]
		d[inc1] += init_d[k]
		d[inc2] += init_d[k]
		d[k] -= init_d[k]
		increase_letter_by(mapping[k], v)
	return d


with open("in.txt") as f:
	frame = f.readline().rstrip()
	f.readline()
	for line in f:
		mapping[line.split(' -> ')[0]] = line.rstrip().split(' -> ')[1]

	d = init_dict(frame)
	for i in range(40):
		nd = step(d)
		d = nd
		if i == 9:
			print("Part1: most common element minus least common element is {}".format(max(letter_cnt.values()) - min(letter_cnt.values())))

	print("Part2: most common element minus least common element is {}".format(max(letter_cnt.values()) - min(letter_cnt.values())))
