import os, sys


current_dir = '/'
sizes = {}


def get_parent_dir(fr):
	assert len(fr) > 0
	if fr == '/' or fr.rfind('/') == 0:
		return '/'
	return str(fr[:fr.rfind('/')])


def add_size_to_dir(d, size):
	if d not in sizes:
		sizes[d] = size
	else:
		sizes[d] += size

	parent = get_parent_dir(d)
	if parent == d:
		return
	add_size_to_dir(parent, size)


with open("in.txt") as file:
	data = [l.rstrip() for l in file]



for i in range(len(data)):
	if '$' in data[i]:
		if 'cd' in data[i]:
			if '..' in data[i]:
				current_dir = get_parent_dir(current_dir)
			else:
				current_dir = os.path.join(current_dir, data[i][5:])

		elif 'ls' in data[i]:
			j = 1
			while '$' not in data[i+j]:
				line = data[i+j]
				if line[0].isdigit():
					add_size_to_dir(current_dir, int(line.split(' ')[0]))
				j += 1
				if i+j >= len(data):
					break


print("Part1: sum of the total sizes of those directories {}".format(sum([sizes[k] for k in sizes.keys() if sizes[k] <= 100000])))

needed_space = 30000000 - (70000000 - sizes['/'])
min_diff = sys.maxsize

for k in sizes.keys():
	if k == '/':
		continue

	if sizes[k] > needed_space:
		d = sizes[k] - needed_space
		if d < min_diff:
			min_diff = d
			smallest = sizes[k]

print("Part2: total size of the directory to remove {}".format(smallest))