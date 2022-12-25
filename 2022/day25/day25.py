
alph = {
	'=': -2,
	'-': -1,
	'0': 0,
	'1': 1,
	'2': 2
}

def to_snafu(d):
	r = ''
	while d:
		rest = d % 5
		d //= 5

		if rest <= 2:
			r = str(rest) + r
		else:
			if rest == 3:
				r = '=' + r
			elif rest == 4:
				r = '-' + r
			d += 1
	return r


def to_digit(d):
	q = 1
	r = 0
	for c in d[::-1]:
		r += q * alph[c]
		q *= 5
	return r


with open('in.txt') as file:
	data = [l.rstrip() for l in file]


s = 0
for d in data:
	s += to_digit(d)

print('Part1: SNAFU number for Bob s console: {}'.format(to_snafu(s)))
