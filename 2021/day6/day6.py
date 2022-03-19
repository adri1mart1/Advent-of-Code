
with open("in.txt") as f:
	fishes = [int(x) for x in f.readline().rstrip().split(',')]

ages = [0 for x in range(9)]

for f in fishes:
	ages[f] += 1

for i in range(256):
	a = ages[0]
	ages = ages[1:]
	ages.append(a)
	ages[6] += a

	if i+1 == 80:
		print("part1: number of fishes after 80 days: {}".format(sum(ages)))

print("part2: number of fishes after 256 days: {}".format(sum(ages)))
