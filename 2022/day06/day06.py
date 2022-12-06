
def func(n, s):
	for i in range(n-1, len(d)-n):
		if len(set(d[i-n+1:i+1])) == n:
			return i+1

with open("in.txt") as file:
	for d in [l.rstrip() for l in file]:
		print("Part1: Starter marker of 4-length at index {}".format(func(4, d)))
		print("Part1: Starter marker of 14-length at index {}".format(func(14, d)))
