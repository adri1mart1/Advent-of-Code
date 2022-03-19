import statistics

with open("in.txt") as f:
	crabs = [int(x) for x in f.readline().rstrip().split(',')]

med = int(statistics.median(crabs))
avg = int(statistics.mean(crabs))

print("part1: fuel spent: {}".format(sum([abs(crabs[i]-med) for i in range(len(crabs))])))

# the sum of 1+2+3+4+..+n is n(n+1)/2
tot = 0
for i in range(len(crabs)):
	tot += abs(crabs[i]-avg)*(abs(crabs[i]-avg)+1)/2

print("part2: fuel spent: {}".format(int(tot)))
