import re

re_digit = re.compile(".*:\ (\d*)$")

with open('in.txt') as file:
    data = [l.rstrip() for l in file]


def yell_num_part1(n, monkey):
    # This is a recursive function that computes monkey's result.
    # In addition, (needed for part 2), it returns an additional bool
    # if my monkey is in left or right subtree.
    assert(len(monkey) == 4)

    for d in data:
        if monkey in d[0:4]:
            m = re_digit.match(d)
            if m:
                return int(m.group(1)), monkey == 'humn'

            a = d.split(' ')
            b, my_monkey_1 = yell_num_part1(n+1, a[1])
            c, my_monkey_2 = yell_num_part1(n+1, a[3])
            return eval('{} {} {}'.format(b, a[2], c)), my_monkey_1 or my_monkey_2

    assert False # could not find monkey in list


def yell_num_part2(n, monkey, expected_num):
    # This is a recursive function that computes both left and right side of
    # the operation. The result from the tree containing my monkey is checked
    # against expected_num, if different, compute the difference and continue
    # recursive subsequent calls.
    assert (len(monkey) == 4)

    if monkey == 'humn':
        return int(expected_num)

    for d in data:
        if monkey in d[0:4]:
            arg1 = d.split(' ')[1]
            operator = d.split(' ')[2]
            arg2 = d.split(' ')[3]
            res_left, monkey_left = yell_num_part1(0, arg1)
            res_right, monkey_right = yell_num_part1(0, arg2)
            assert monkey_left or monkey_right, "could not find monkey anywhere"
            monkey_search = arg1 if monkey_left else arg2

            if monkey == 'root':
                new_expected_num = res_right if monkey_left else res_left
            else:
                # ex: 150 = 8 / 4
                if operator == '/':
                    if monkey_left:
                        new_expected_num = expected_num * res_right
                    else:
                        new_expected_num = expected_num / res_left

                # ex: 150 = 8 + 4
                elif operator == '+':
                    if monkey_left:
                        new_expected_num = expected_num - res_right
                    else:
                        new_expected_num = expected_num - res_left

                # ex: 150 = 8 - 4
                elif operator == '-':
                    if monkey_left:
                        new_expected_num = expected_num + res_right
                    else:
                        new_expected_num = res_left - expected_num

                # ex: 596 = 8 * 4
                else:
                    if monkey_left:
                        new_expected_num = expected_num / res_right
                    else:
                        new_expected_num = expected_num / res_left

            return yell_num_part2(n+1, monkey_search, new_expected_num)

    assert False


print('Part1: number the monkey named root yell: {}'.format(int(yell_num_part1(0, 'root')[0])))
print('Part2: to pass root equality, i need to yell {}'.format(yell_num_part2(0, 'root', 0)))
