import sys

# Part2 is definitely not the best in terms of performance. My current implementation find all
# 'a' starting point and measure the path to the end 'E'. The min result is displayed.
# This is stupid to rerun so many times the shortest path algo but the execution time is about
# 2min with the provided example and i didn't push further.
# However, a better approach would have been to start from 'E' and stop when any 'a' is found.
# This means update the shortest_path() function so it works in both ascendant and descendant
# way.

with open("in.txt") as file:
    mat = [list(map(str, l.rstrip())) for l in file.readlines()]


def get_start_pos(letter):
    for x in range(len(mat)):
        for y in range(len(mat[0])):
            if mat[x][y] == letter:
                return x, y
    assert False


def get_diff(x, y, letter):
    if mat[x][y] == 'E':
        return ord('z')-ord(letter)
    return ord(mat[x][y])-ord(letter)


def shortest_path(start_pos, end_letter):
    visited = []
    queue = []
    visited.append(start_pos)
    queue.append([start_pos])

    while queue:
        path = queue.pop(0)
        p = path[-1]
        val = mat[p[0]][p[1]]

        if val == 'S':
            val = 'a'
        if val == end_letter:
            return len(path)-1

        # check up
        if p[0]-1 >= 0:
            diff = get_diff(p[0]-1, p[1], val)
            if diff < 2 and (p[0]-1, p[1]) not in visited:
                new_path = list(path)
                new_path.append((p[0]-1, p[1]))
                queue.append(new_path)
                visited.append((p[0]-1, p[1]))

        # check down
        if p[0]+1 < len(mat):
            diff = get_diff(p[0]+1, p[1], val)
            if diff < 2 and (p[0]+1, p[1]) not in visited:
                new_path = list(path)
                new_path.append((p[0]+1, p[1]))
                queue.append(new_path)
                visited.append((p[0]+1, p[1]))

        # check left
        if p[1]-1 >= 0:
            diff = get_diff(p[0], p[1]-1, val)
            if diff < 2 and (p[0], p[1]-1) not in visited:
                new_path = list(path)
                new_path.append((p[0], p[1]-1))
                queue.append(new_path)
                visited.append((p[0], p[1]-1))

        # check right
        if p[1]+1 < len(mat[0]):
            diff = get_diff(p[0], p[1]+1, val)
            if diff < 2 and (p[0], p[1]+1) not in visited:
                new_path = list(path)
                new_path.append((p[0], p[1]+1))
                queue.append(new_path)
                visited.append((p[0], p[1]+1))

    return sys.maxsize # return a max length in case end is unreachable


p1 = shortest_path(get_start_pos('S'), 'E')
print("Part1: fewest steps required to move from any 'S' to 'E': {}".format(p1))

start_points = []
for x in range(len(mat)):
    for y in range(len(mat[0])):
        if mat[x][y] == 'a':
            start_points.append((x, y))

paths = []

for start in start_points:
    paths.append(shortest_path(start, 'E'))

print("Part2: fewest steps required to move from any 'a' to 'E': {}".format(min(paths)))
