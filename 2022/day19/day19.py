import time
from dataclasses import dataclass
import queue

# this way was quite interesting. Running a BFS and pruning branches that are not very interesting.
# I had quite some difficulties with the pruning part. I've tried to prune when hitting too many
# resources, but I couldn't get the right answer. The problem initially state you take one minute
# to build a robot but could you build multiple robot per minute, that was a bit ambiguous in my
# initial reflexion.
# My algorithm prune all results with too many robot. Say on each turn we can spent 5 resources,
# we never need more than 5 robot of this type then.
# 2nd pruning function is, when we can build a geode robot, that's the best move, we don't even
# consider other states.
# 3rd pruning is a bit obvious but we use a set() to store all states that have been visited. Don't
# visit the same state twice.
# 4th pruning is working thanks to god ! I have a list 'best_geode_per_turn' that have 32 slots. Each
# slot store the biggest number of geode that have been seen on that turn. We consider that, at a
# turn N, if a state has too less geodes, it will never catch back its delay to get new geodes.
# This pruning idea gives the right result but it definitely not the best !

# Note: Execution time on a 16 core, i7-11850, 2,5GHz is about 5min30 for both part 1 and part 2

results = set()
minute = 0
ore = 1
clay = 2
obsi = 3
geode = 4
ore_robot = 5
clay_robot = 6
obsi_robot = 7
geode_robot = 8
best_geode_per_turn = [0 for _ in range(33)]


@dataclass
class Costs:
    ore_robot_ore_cost: int
    clay_robot_ore_cost: int
    obsidian_robot_ore_cost: int
    obsidian_robot_clay_cost: int
    geode_robot_ore_cost: int
    geode_robot_obsidian_cost: int

    def print(self):
        print('Each ore robot costs {} ore.'.format(self.ore_robot_ore_cost))
        print('Each clay robot costs {} ore.'.format(self.clay_robot_ore_cost))
        print('Each obsidian robot costs {} ore and {} clay.'.format(self.obsidian_robot_ore_cost,
                                                                     self.obsidian_robot_clay_cost))
        print('Each geode robot costs {} ore and {} obsidian.'.format(self.geode_robot_ore_cost,
                                                                      self.geode_robot_obsidian_cost))


def analyse_tuple(costs: Costs, start, n_turns):
    global best_geode_per_turn

    max_ore_cost = max([costs.ore_robot_ore_cost, costs.clay_robot_ore_cost, costs.obsidian_robot_ore_cost, costs.geode_robot_ore_cost])
    max_clay_cost = costs.obsidian_robot_clay_cost
    max_obsi_cost = costs.geode_robot_obsidian_cost

    q = queue.Queue()
    q.put(start)

    seen = set()
    best_geode_per_turn = [0 for _ in range(n_turns+1)]

    while not q.empty():
        item = q.get()

        if item in seen:
            continue

        m, ore, cla, obs, geo, ror, rcl, rob, rge = item
        seen.add((m, ore, cla, obs, geo, ror, rcl, rob, rge))

        best_geode_per_turn[m] = max(best_geode_per_turn[m], geo)

        # end reached
        if m >= n_turns:
            results.add((m, ore, cla, obs, geo, ror, rcl, rob, rge))
            continue

        # pruning too many unneeded robots
        if ror > max_ore_cost:
            continue
        if rcl > max_clay_cost:
            continue
        if rob > max_obsi_cost:
            continue

        # pruning all items that have less than 2 geode at a specific turn. This means the item
        # has too much delay in acquiring geodes so don't even bother continuing on this branch.
        # Definitely not the best pruning idea, but it works quite well in comparison
        # with what I've seen so far.
        if geo < best_geode_per_turn[m]-2:
            continue

        # build geode robot
        if ore >= costs.geode_robot_ore_cost and obs >= costs.geode_robot_obsidian_cost:
            q.put((m + 1, ore - costs.geode_robot_ore_cost + ror, cla + rcl,
                   obs - costs.geode_robot_obsidian_cost + rob, geo + rge, ror, rcl, rob, rge + 1))
            # continue here because this is probably the best move to do, don't even bother checking other moves
            continue

        # build obsidian robot
        if ore >= costs.obsidian_robot_ore_cost and cla >= costs.obsidian_robot_clay_cost:
            q.put((m + 1, ore - costs.obsidian_robot_ore_cost + ror, cla - costs.obsidian_robot_clay_cost + rcl,
                   obs + rob, geo + rge, ror, rcl, rob + 1, rge))

        # build clay robot
        if ore >= costs.clay_robot_ore_cost:
            q.put((m + 1, ore - costs.clay_robot_ore_cost + ror, cla + rcl, obs + rob, geo + rge, ror, rcl + 1, rob,
                   rge))

        # build ore robot
        if ore >= costs.ore_robot_ore_cost:
            q.put((m + 1, ore - costs.ore_robot_ore_cost + ror, cla + rcl, obs + rob, geo + rge, ror + 1, rcl, rob,
                   rge))

        # build nothing
        q.put((m + 1, ore + ror, cla + rcl, obs + rob, geo + rge, ror, rcl, rob, rge))

    print("best geode per turn: {}".format(best_geode_per_turn))


with open('in.txt') as file:
    data = [l.rstrip() for l in file]

i = 0
s1 = 0
s2 = 1

for d in data:
    print('\n{}'.format(d))
    i += 1

    bp_costs = Costs(int(d.split(' ')[6]), int(d.split(' ')[12]), int(d.split(' ')[18]), int(d.split(' ')[21]),
                     int(d.split(' ')[27]), int(d.split(' ')[30]))
    bp_costs.print()

    # some asserts just to be just inputs are always for the same resource type
    assert d.split(' ')[3] == 'ore'
    assert d.split(' ')[7] == 'ore.'
    assert d.split(' ')[9] == 'clay'
    assert d.split(' ')[13] == 'ore.'
    assert d.split(' ')[15] == 'obsidian'
    assert d.split(' ')[19] == 'ore'
    assert d.split(' ')[22] == 'clay.'
    assert d.split(' ')[24] == 'geode'
    assert d.split(' ')[28] == 'ore'
    assert d.split(' ')[31] == 'obsidian.'

    results = set()

    n = 32 if i <= 3 else 24

    start_time = time.time()
    analyse_tuple(bp_costs, (0, 0, 0, 0, 0, 1, 0, 0, 0), n)
    print("depth: {} - time: {} seconds ---".format(n, time.time() - start_time))
    print("best_geode: {}".format(best_geode_per_turn[n]))

    if i <= 3:
        s2 *= best_geode_per_turn[32]
    s1 += best_geode_per_turn[24] * i

print('\n\n')
print('part1: the quality level of each blueprint using the largest number of geodes it could produce in 24 '
      'minutes is {}'.format(s1))

print('part2: depth-32, the multiplication of largest geodes number for the first 3 blueprints is {}'.format(s2))
