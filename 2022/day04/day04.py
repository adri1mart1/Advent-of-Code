
if __name__ == "__main__":

	with open("in.txt") as file:
		data = [l.rstrip() for l in file]

	score_p1 = score_p2 = 0

	for d in data:
		p1 = d.split(',')[0]
		p2 = d.split(',')[1]

		p1_min = int(p1.split('-')[0])
		p1_max = int(p1.split('-')[1])
		p2_min = int(p2.split('-')[0])
		p2_max = int(p2.split('-')[1])

		if  (p1_min >= p2_min and p1_max <= p2_max) or (p2_min >= p1_min and p2_max <= p1_max):
			score_p1 += 1

		if p2_min <= p1_max and p2_max >= p1_min:
			score_p2 += 1

	print("Part1: Number of pairs that fully contains the other: {}".format(score_p1))
	print("Part2: Number of pairs that overlaps: {}".format(score_p2))
