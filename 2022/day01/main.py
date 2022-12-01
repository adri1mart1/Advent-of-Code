
elf = 0
top_elves = []


def check_elf():
	if len(top_elves) < 3:
		top_elves.append(elf)
	else:
		for i in range(0, 3):
			if elf > top_elves[i]:
				top_elves[i] = elf
				break


if __name__ == '__main__':

	data = []

	with open("in.txt") as f:
		for line in f.readlines():
			data.append(line.rstrip())

	for d in data:
		if d != '':
			elf += int(d)
			continue
		else:
			check_elf()
			elf = 0

	# check the very last elf
	check_elf()

	top_elves.sort()

	print("Part 1: Most carying calories by an elf: {}".format(top_elves[-1]))
	print("Part 2: Sum of top 3 elves: {}".format(sum(top_elves)))
