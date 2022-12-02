
win_score = 6
draw_score = 3

rock_score = 1
paper_score = 2
scissors_score = 3


def is_rock(letter):
	return letter == 'A' or letter == 'X'

def is_paper(letter):
	return letter == 'B' or letter == 'Y'

def is_scissors(letter):
	return letter == 'C' or letter == 'Z'

def lost_expected(letter):
	return letter == 'X'

def draw_expected(letter):
	return letter == 'Y'

def win_expected(letter):
	return letter == 'Z'


if __name__ == "__main__":

	with open('in.txt') as file:
		data = [l.rstrip() for l in file]

	total_p1 = 0
	total_p2 = 0

	for d in data:
		me = d[2]
		opp = d[0]

		score_p1 = 0
		score_p2 = 0

		if is_rock(opp):

			if is_rock(me):
				score_p1 += rock_score
				score_p1 += draw_score
			elif is_paper(me):
				score_p1 += paper_score
				score_p1 += win_score
			elif is_scissors(me):
				score_p1 += scissors_score

			if lost_expected(me):
				score_p2 += scissors_score
			elif draw_expected(me):
				score_p2 += draw_score
				score_p2 += rock_score
			elif win_expected(me):
				score_p2 += win_score
				score_p2 += paper_score

		if is_paper(opp):

			if is_rock(me):
				score_p1 += rock_score
			elif is_paper(me):
				score_p1 += paper_score
				score_p1 += draw_score
			elif is_scissors(me):
				score_p1 += scissors_score
				score_p1 += win_score

			if lost_expected(me):
				score_p2 += rock_score
			elif draw_expected(me):
				score_p2 += draw_score
				score_p2 += paper_score
			elif win_expected(me):
				score_p2 += win_score
				score_p2 += scissors_score

		if is_scissors(opp):

			if is_rock(me):
				score_p1 += rock_score
				score_p1 += win_score
			elif is_paper(me):
				score_p1 += paper_score
			elif is_scissors(me):
				score_p1 += scissors_score
				score_p1 += draw_score

			if lost_expected(me):
				score_p2 += paper_score
			elif draw_expected(me):
				score_p2 += draw_score
				score_p2 += scissors_score
			elif win_expected(me):
				score_p2 += win_score
				score_p2 += rock_score

		total_p1 += score_p1
		total_p2 += score_p2

	print("Part 01: rock paper scissors score: {}".format(total_p1))
	print("Part 02: rock paper scissors score: {}".format(total_p2))
