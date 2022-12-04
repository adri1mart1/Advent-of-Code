
def get_value(letter):
    if letter.islower():
        return ord(letter) - ord('a') + 1
    return ord(letter) - ord('A') + 26 + 1


if __name__ == "__main__":

    with open('in.txt') as file:
        data = [l.rstrip() for l in file]

    total = 0

    for line in data:
        assert(len(line)%2 == 0)
        mid = int(len(line)/2)
        letter = list(set(line[:mid]).intersection(line[mid:]))[0]
        total += get_value(letter)

    print("Part1: sum of priorities of these items: {}".format(total))

    total = 0

    assert(len(data)%3 == 0)
    for i in range(0, int(len(data)/3)):
        first = data[0+3*i]
        second = data[1+3*i]
        third = data[2+3*i]

        common_A = set(first).intersection(second)
        common_all = common_A.intersection(third)
        badge = list(common_all)[0]
        total += get_value(badge)

    print("Part2: sum of priorities of these items: {}".format(total))
