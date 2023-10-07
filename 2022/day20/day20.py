
# I had troubles with this puzzle even though, at first sight, it doesn't look so difficult.
# The first version I made was switching N time to the left or to the right. I got obviously stuck
# on part 2 with this huge multiplier factor.
# I ended up on a solution easy to find, updating only final nodes and its neighbours but I faced a
# 2 bugs hard to find with official input. training input has only numbers below total length so that
# was ok but as soon as modulus was in the game, I had troubles.
# The second bug was about having a number that stay in the exact same pos but different from zero.
# A nightmare to debug, I had to compare with an existing program to found out this.
# Quite interesting in the end, but I need to be more careful.

nodes_p1 = []
nodes_p2 = []
node_len = 0


class Node:
    def __init__(self, num):
        self.num = num
        self.left = None
        self.right = None


with open("in.txt") as f:
    data = [int(l.rstrip()) for l in f]

    for i in range(len(data)):
        nodes_p1.append(Node(data[i]))
        nodes_p2.append(Node(data[i] * 811589153))

# add all neighbors
for i in range(len(nodes_p2)):
    nodes_p1[i].left = nodes_p1[(i-1) % len(nodes_p1)]
    nodes_p1[i].right = nodes_p1[(i+1) % len(nodes_p1)]
    nodes_p2[i].left = nodes_p2[(i-1) % len(nodes_p2)]
    nodes_p2[i].right = nodes_p2[(i+1) % len(nodes_p2)]

node_len = len(nodes_p2)


def mix(ns):
    for n in ns:
        ptr = n

        if n.num == 0:
            pass

        elif n.num > 0:
            for _ in range(n.num % (node_len-1)):
                ptr = ptr.right
            if ptr != n:
                n.left.right = n.right
                n.right.left = n.left
                n.left = ptr
                n.right = ptr.right
                ptr.right.left = n
                ptr.right = n

        elif n.num < 0:
            for _ in range((-n.num) % (node_len-1)):
                ptr = ptr.left

            if ptr != n:
                n.left.right = n.right
                n.right.left = n.left
                n.left = ptr.left
                n.right = ptr
                ptr.left.right = n
                ptr.left = n

    return ns


def find_idx_zero(nodes):
    r = 0
    for i in range(len(nodes)):
        if nodes[i].num == 0:
            break
        r += 1
    return r


def get_groove_coord(nodes, idx_zero):
    i = 1
    s = 0
    ptr = nodes[idx_zero]
    while True:
        ptr = ptr.right
        if i in [1000, 2000, 3000]:
            s += ptr.num
            if i == 3000:
                break
        i += 1
    return s


# part 1
nodes_p1 = mix(nodes_p1)
idx_zero = find_idx_zero(nodes_p1)

print("Part1: The groove coordinates are {}".format(get_groove_coord(nodes_p1, idx_zero)))

# part 2
for _ in range(10):
    nodes_p2 = mix(nodes_p2)
idx_zero = find_idx_zero(nodes_p2)

print("Part2: The groove coordinates are {}".format(get_groove_coord(nodes_p2, idx_zero)))
