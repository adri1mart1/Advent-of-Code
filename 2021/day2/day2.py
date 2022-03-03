h1, d1, h2, d2, aim = 0, 0, 0, 0, 0

with open("in.txt") as f:
	for line in f:
		val = int(line.rstrip()[-1])
		if "up" in line:
			d1 -= val
			aim -= val
		elif "down" in line:
			d1 += val
			aim += val
		elif "forward" in line:
			h1 += val
			h2 += val
			d2 += aim*val
print(f"part1: horizontal pos: {h1} depth: {d1} product: {h1*d1}")
print(f"part2: horizontal pos: {h2} depth: {d2} aim:{aim} product: {h2*d2}")
