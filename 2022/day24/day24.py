import copy

# definitely not my best code ever !

# considering x -> horizontal and y -> vertical
blizards = set()     # tuple of ((x, y), dir)
blizards_pos = set() # tuple of (x, y) only (easier to get blizards pos faster)

with open('in.txt') as file:
    data = [l.rstrip() for l in file]
    raw_map = copy.deepcopy(data)

for i in range(len(raw_map)):
    raw_map[i] = raw_map[i].replace('<', '.').replace('>', '.').replace('v','.').replace('^', '.')

y_max = len(data)
x_max = len(data[1])


def blizards_next(bliz):
    new_bliz = set()     # tuple of ((x, y), dir)
    new_bliz_pos = set() # tuple of (x, y)
    for b in bliz:
        if b[1] == '>':
            new_x = (b[0][0] + 1) % (x_max - 1)
            new_x += 1 if new_x == 0 else 0
            new_bliz.add(((new_x, b[0][1]), b[1]))
            new_bliz_pos.add((new_x, b[0][1]))
        elif b[1] == '<':
            new_x = b[0][0] - 1
            new_x += x_max - 2 if new_x == 0 else 0
            new_bliz.add(((new_x, b[0][1]), b[1]))
            new_bliz_pos.add((new_x, b[0][1]))
        elif b[1] == 'v':
            new_y = (b[0][1] + 1) % (y_max - 1)
            new_y += 1 if new_y == 0 else 0
            new_bliz.add(((b[0][0], new_y), b[1]))
            new_bliz_pos.add((b[0][0], new_y))
        elif b[1] == '^':
            new_y = b[0][1] - 1
            new_y += y_max - 2 if new_y == 0 else 0
            new_bliz.add(((b[0][0], new_y), b[1]))
            new_bliz_pos.add((b[0][0], new_y))
        else:
            assert False
    return new_bliz, new_bliz_pos


def is_valid_move(m):
    # check out of bound
    if m[0] < 0 or m[0] >= x_max or m[1] < 0 or m[1] >= y_max:
        return False
    # check is in map and no blizards
    return raw_map[m[1]][m[0]] == '.' and m not in blizards_pos


# add all blizards to lists
for x in range(1, x_max-1):
    for y in range(1, y_max-1):
        c = data[y][x]
        if c != '.':
            blizards.add(((x, y), c))
            blizards_pos.add((x, y))


def reach_goal(fr, to):
    global blizards, blizards_pos
    nturn = 0
    pos = set()
    pos.add(fr)

    while True:
        nturn += 1
        blizards, blizards_pos = blizards_next(blizards)
        next_pos = set()

        for p in pos:
            for m in [(p[0]-1,p[1]), (p[0]+1,p[1]), (p[0],p[1]-1), (p[0],p[1]+1), p]:
                if m == to:
                    return nturn
                if is_valid_move(m):
                    next_pos.add(m)
        pos = next_pos

start = (1, 0)
end = (x_max-2, y_max-1)

p1 = reach_goal(start, end)
p2 = p1 + reach_goal(end, start) + reach_goal(start, end)

print('part1: the fewest number of minutes required to avoid the blizzards and reach the goal is {}'.format(p1))
print('part2: the fewest number of minutes required to reach the goal, go back to the start, then reach the goal again is {}'.format(p2))
