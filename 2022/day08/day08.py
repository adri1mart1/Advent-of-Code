
def get_visibility_and_score(row, col, start, stop, step, horizontal):
	score = 0
	visible = True
	for i in range(start, stop, step):
		score += 1
		if horizontal:
			if data[row][i] >= data[row][col]:
				visible = False
				break
		else:
			if data[i][col] >= data[row][col]:
				visible = False
				break
	return (visible, score)

with open("in.txt") as file:
	data = [list(map(int, l.rstrip())) for l in file.readlines()]

rows = len(data[0])
cols = len(data)

visible_num = 0
sweet_spot = 0

for row in range(cols):
	for col in range(rows):
		left   = get_visibility_and_score(row, col, col-1, -1,  -1, True)
		right  = get_visibility_and_score(row, col, col+1, cols, 1, True)
		top    = get_visibility_and_score(row, col, row-1, -1,  -1, False)
		bottom = get_visibility_and_score(row, col, row+1, rows, 1, False)

		if left[0] or right[0] or top[0] or bottom[0]:
			visible_num += 1

		sweet_spot = max(left[1] * right[1] * top[1] * bottom[1], sweet_spot)

print('Part1: Number of visible {}'.format(visible_num))
print('Part2: Sweet spot score {}'.format(sweet_spot))
