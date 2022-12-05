import copy


# original answer, inputs were hardcoded
stacks_p1 = [
	['Z', 'N'],
	['M', 'C', 'D'],
	['P']
]

stacks_p2 = [
	['D','M','S','Z','R','F','W','N'],
	['S','G','Q','P','W'],
	['W','R','V','Q','F','N','J','C'],
	['F','Z','P','C','G','D','L'],
	['T','P','S'],
	['H','D','F','W','R','L'],
	['Z','N','D','C'],
	['W','N','R','F','V','S','J','Q'],
	['R','M','S','G','Z','W','V']
]

stacks = copy.deepcopy(stacks_p2) # switch from example to real stuff


def move_part1(n, fr, to):
	for i in range(n):
		stacks[to-1].append(stacks[fr-1].pop())


def move_part2(n, fr, to):
	values = []
	for i in range(n):
		values.append(stacks[fr-1].pop())

	for i in range(len(values)):
		stacks[to-1].append(values[-i-1])


def print_last(header):
	print(header, end='')
	for i in range(len(stacks)):
		print(stacks[i][-1], end='')
	print()


if __name__ == "__main__":

	with open("in.txt") as file:
		lines = [l.rstrip() for l in file]

	for l in lines:
		if 'move' in l:
			move_part1(int(l.split(' ')[1]), int(l.split(' ')[3]), int(l.split(' ')[5]))
	print_last("Part1: crate ends up on top of each stack ")

	stacks = stacks_p2

	for l in lines:
		if 'move' in l:
			move_part2(int(l.split(' ')[1]), int(l.split(' ')[3]), int(l.split(' ')[5]))
	print_last("Part2: crate ends up on top of each stack ")
