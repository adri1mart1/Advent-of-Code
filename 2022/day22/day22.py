import re

# part2 was quite difficult to get, so I searched some info on internet and found out the easiest way is to hardcode
# some key parameters. I got my inspiration from hyper neutrino's video explaining the concept.

official_input = 'in.txt'
training_input = 'in2.txt'
current_input = official_input
# square size
sqs = 4 if current_input == training_input else 50

with open(current_input) as file:
    data = [l.rstrip() for l in file]

col_max = 0
row_max = len(data) - 2

mat = [[] for _ in range(row_max)]
instructions_str = ""
instructions = None

# save map in a matrix
i = 0
for i in range(len(data)):
    if data[i] == '':
        instructions_str = data[i + 1]
        break
    for c in data[i]:
        mat[i].append(c)
    col_max = max(col_max, len(data[i]))
    i += 1

# allocate missing spots
for row in range(row_max):
    for col in range(col_max):
        for i in range(col_max - len(mat[row])):
            mat[row].append(' ')


def print_mat():
    for r in range(row_max):
        for c in range(col_max):
            print(mat[r][c], end='')
        print()


def get_direction_number():
    if dr == 0 and dc == 1:
        return 0
    if dr == 1 and dc == 0:
        return 1
    if dr == 0 and dc == -1:
        return 2
    if dr == -1 and dc == 0:
        return 3
    return -1


def moving(row, col, num, part):
    global dr, dc
    nc, nr, ndr, ndc, ri = col, row, dr, dc, 0

    while True:
        if ri == num:
            break

        if part == 1:
            nc = (nc + dc) % col_max
            nr = (nr + dr) % row_max

        elif part == 2:
            nc = nc + dc
            nr = nr + dr

            if current_input == training_input:
                #                             1__________2
                #                             |          |
                #                             |          |
                #                             |          |
                #       2__________1__________|__________|5
                #       |          |          |6         |
                #       |          |          |          |
                #       |          |          |          |
                #       |__________|__________|7________8|__________5
                #       4          3          |          |          |
                #                             |          |          |
                #                             |          |          |
                #                            3|__________|__________|
                #                                        4          2

                # top 1-2 segment going up
                if nr < 0 and 2 * sqs <= nc < 3 * sqs and dr == -1 and dc == 0:
                    nr = sqs
                    nc = 3 * sqs - nc
                    ndr, ndc = 1, 0

                # middle 2-1 segment going up
                elif nr < sqs and 0 <= nc < sqs and dr == -1 and dc == 0:
                    nr = 0
                    nc = 3 * sqs - nc
                    ndr, ndc = 1, 0

                # top 2-5 segment going right
                elif nc >= 3 * sqs and 0 <= nr < sqs and dr == 0 and dc == 1:
                    nr = 3 * sqs - nr - 1
                    nc = 4 * sqs - 1
                    ndr, ndc = 0, -1

                # down 2-5 segment going right
                elif nc >= 4 * sqs and 2 * sqs <= nr < 3 * sqs and dr == 0 and dc == 1:
                    nr = - nr - sqs
                    nc = 3 * sqs - 1
                    ndr, ndc = 0, -1

                # left 4-3 seg going down
                elif nr >= 2 * sqs and 0 <= nc < sqs and dr == 1 and dc == 0:
                    nr = 3 * sqs - 1
                    nc = 3 * sqs - nc - 1
                    ndr, ndc = -1, 0

                # lower 4-3 seg going down
                elif nr >= 3 * sqs and 2 * sqs <= nc < 3 * sqs and dr == 1 and dc == 0:
                    nr = 2 * sqs - 1
                    nc = 3 * sqs - nc - 1
                    ndr, ndc = -1, 0

                # 4-2 seg left
                elif nc < 0 and sqs <= nr < 2 * sqs and dr == 0 and dc == -1:
                    nc = 5 * sqs - nr - 1
                    nr = 3 * sqs - 1
                    ndr, ndc = -1, 0

                # 4-2 seg down
                elif nr >= 3 * sqs and 3 * sqs <= nc < 4 * sqs and dr == 1 and dc == 0:
                    nr = 5 * sqs - nc - 1
                    nc = 0
                    ndr, ndc = 0, 1

                # 1-6 seg left
                elif nc < 2 * sqs and 0 <= nr < sqs and dr == 0 and dc == -1:
                    nc = nr + sqs
                    nr = sqs
                    ndr, ndc = 1, 0

                # 1-6 seg up
                elif nr < sqs and sqs <= nc < 2 * sqs and dr == -1 and dc == 0:
                    nr = nc - sqs
                    nc = 2 * sqs
                    ndr, ndc = 0, 1

                # 3-7 down
                elif nr >= 2 * sqs and sqs <= nc < 2 * sqs and dr == 1 and dc == 0:
                    nr = 4 * sqs - nc - 1
                    nc = 2 * sqs
                    ndr, ndc = 0, 1

                # 3-7 left
                elif nc < 2 * sqs and 2 * sqs <= nr < 3 * sqs and dr == 0 and dc == -1:
                    nc = 4 * sqs - nr - 1
                    nr = 2 * sqs
                    ndr, ndc = -1, 0

                # 8-5 right
                elif nc >= 3 * sqs and sqs <= nr < 2 * sqs and dr == 0 and dc == 1:
                    nc = 5 * sqs - nr - 1
                    nr = 2 * sqs
                    ndr, ndc = 1, 0

                # 8-5 up
                elif nr < 2 * sqs and 3 * sqs <= nc < 4 * sqs and dr == -1 and dc == 0:
                    nr = 5 * sqs - nc - 1
                    nc = 3 * sqs - 1
                    ndr, ndc = 0, -1

            elif current_input == official_input:
                #                  1__________5__________3
                #                  |          |          |
                #                  |          |          |
                #                  |          |          |
                #                 2|__________6__________|4
                #                  |          |
                #                  |          |
                #                  |          |
                #       2__________7__________|4
                #       |          |          |
                #       |          |          |
                #       |          |          |
                #      1|__________8__________|3
                #       |          |
                #       |          |
                #       |          |
                #      5|__________|3

                # top 1-5 seg, going up
                if nr < 0 and sqs <= nc < 2 * sqs and dr == -1 and dc == 0:
                    nr = nc + 2 * sqs
                    nc = 0
                    ndr, ndc = 0, 1

                # left 1-5 seg, going left
                elif nc < 0 and 3 * sqs <= nr < 4 * sqs and dr == 0 and dc == -1:
                    nc = nr - 2 * sqs
                    nr = 0
                    ndr, ndc = 1, 0

                # top 5-3 seg, going up
                elif nr < 0 and 2 * sqs <= nc < 3 * sqs and dr == -1 and dc == 0:
                    nr = 4 * sqs - 1
                    nc = nc - 2 * sqs
                    ndr, ndc = -1, 0

                # down 5-3 seg, going down
                elif nr >= 4 * sqs and 0 <= nc < sqs and dr == 1 and dc == 0:
                    nr = 0
                    nc = nc + 2 * sqs
                    ndr, ndc = 1, 0

                # left 1-2 seg, going left
                elif nc < 0 and 2 * sqs <= nr < 3 * sqs and dr == 0 and dc == -1:
                    nr = sqs - (nr - 2 * sqs) - 1
                    nc = sqs
                    ndr, ndc = 0, 1

                # middle 1-2 seg, going left
                elif nc < sqs and 0 <= nr < sqs and dr == 0 and dc == -1:
                    nr = (sqs - nr) + 2 * sqs - 1
                    nc = 0
                    ndr, ndc = 0, 1

                # left 2-7 seg, going up
                elif nr < 2 * sqs and 0 <= nc < sqs and dr == -1 and dc == 0:
                    nr = sqs + nc
                    nc = sqs
                    ndr, ndc = 0, 1

                # middle 2-7 seg, going left
                elif nc < sqs and sqs <= nr < 2 * sqs and dr == 0 and dc == -1:
                    nc = nr - sqs
                    nr = 2 * sqs
                    ndr, ndc = 1, 0

                # middle 8-3 seg, going right
                elif nc >= sqs and 3 * sqs <= nr < 4 * sqs and dr == 0 and dc == 1:
                    nc = nr - 2 * sqs
                    nr = 3 * sqs - 1
                    ndr, ndc = -1, 0

                # right 8-3 seg, going down
                elif nr >= 3 * sqs and sqs <= nc < 2 * sqs and dr == 1 and dc == 0:
                    nr = nc + 2 * sqs
                    nc = sqs - 1
                    ndr, ndc = 0, -1

                # right 4-3 seg, going right
                elif nc >= 3 * sqs and 0 <= nr < sqs and dr == 0 and dc == 1:
                    nr = 3 * sqs - nr - 1
                    nc = 2 * sqs - 1
                    ndr, ndc = 0, -1

                # middle 4-3 seg, going right
                elif nc >= 2 * sqs and 2 * sqs <= nr < 3 * sqs and dr == 0 and dc == 1:
                    nr = 3 * sqs - nr - 1
                    nc = 3 * sqs - 1
                    ndr, ndc = 0, -1

                # right 6-4 seg, going down
                elif nr >= sqs and 2 * sqs <= nc < 3 * sqs and dr == 1 and dc == 0:
                    nr = nc - sqs
                    nc = 2 * sqs - 1
                    ndr, ndc = 0, -1

                # middle 6-4 seg, going right
                elif nc >= 2 * sqs and sqs <= nr < 2 * sqs and dr == 0 and dc == 1:
                    nc = sqs + nr
                    nr = sqs - 1
                    ndr, ndc = -1, 0

        # if we face an empty spot, continue moving sill we find a valid spot
        if mat[nr][nc] == ' ':
            continue

        # if we face a wall, do not move, break loop
        if mat[nr][nc] == '#':
            break

        # else, this must be a valid empty tile so do the actual move
        assert mat[nr][nc] == '.'
        col, row, dr, dc = nc, nr, ndr, ndc
        ri += 1

    return row, col


instructions_str = 'R' + instructions_str  # we always start facing right
r = re.compile(r'([A-Z]\d*)')
instructions = re.findall(r, instructions_str)

for part in range(1, 3):

    # find starting point, the left most valid coord on first row
    row, col = 0, 0
    while mat[row][col] != '.':
        col += 1

    # we initially face right, but we add an extra R to the instructions below
    dr, dc = -1, 0

    for ins in instructions:
        rotation_letter = ins[0]
        num = int(ins[1:])

        # hack from hyper neutrino
        if rotation_letter == "R":
            dr, dc = dc, -dr
        elif rotation_letter == "L":
            dr, dc = -dc, dr

        row, col = moving(row, col, num, part)

    # The final password is the sum of 1000 times the row, 4 times the column, and the facing.
    res = (row + 1) * 1000 + (col + 1) * 4 + get_direction_number()
    print('Part{}: the final password is {}'.format(part, res))
