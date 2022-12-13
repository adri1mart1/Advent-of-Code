import ast
from functools import cmp_to_key

# This day caused me quite a lot of troubles to find the part1. My original
# code was finding correctly the expected number for the example but not the
# main one.
# I ended comparing my solution with a friend and find out my recursive
# function was wrong for 2 reasons.
# I was comparing list in my recursive function. I ran into problems when
# the list was empty and or list of empty list.
# Seeing what others have been doing, i have reworked the function to compare
# values instead of list and call the recursive function till the list is
# not a list anymore

def analyse_pair(p1, p2):
	if type(p1) == list and type(p2) == list:
		for i in range(min(len(p1), len(p2))):
			res = analyse_pair(p1[i], p2[i])
			if res != 0:
				return res
		return analyse_pair(len(p1), len(p2))

	elif type(p1) == int and type(p2) == list:
		return analyse_pair([p1], p2)

	elif type(p1) == list and type(p2) == int:
		return analyse_pair(p1, [p2])

	if p1 == p2:
		return 0
	elif p1 < p2:
		return 1
	else:
		return -1

with open('in.txt') as file:
	data = [l.rstrip() for l in file.readlines()]

part1 = 0
pairs = []
for i in range(0, len(data), 3):
	pairs.append(ast.literal_eval(data[i]))
	pairs.append(ast.literal_eval(data[i+1]))

	if analyse_pair(pairs[-2], pairs[-1]) == 1:
		part1 += i//3+1

fp = [[2]]
lp = [[6]]
pairs.append(fp)
pairs.append(lp)

sorted_pairs = sorted(pairs, reverse=True, key=cmp_to_key(analyse_pair))

for i in range(len(sorted_pairs)):
	if sorted_pairs[i] == fp:
		part2 = i+1
	if sorted_pairs[i] == lp:
		part2 *= i+1
		break

print('Part1: sum of indices of those pairs: {}'.format(part1))
print('Part2: decoder key for the distress signal: {}'.format(part2))
