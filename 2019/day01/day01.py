from math import floor

with open("in.txt") as f:
	arr = [int(l.rstrip()) for l in f]

# testing array
# arr = [12,14,1969, 100756]

def get_fuel(v: int) -> int:
	return floor(v/3) - 2

total_p1 = sum([get_fuel(a) for a in arr])

total_p2 = 0
for a in arr:
	total = 0
	while True:
		na = get_fuel(a)
		if na <= 0:
			total_p2 += total
			break
		a = na
		total += a

print("part1: {}".format(total_p1))
print("part2: {}".format(total_p2))