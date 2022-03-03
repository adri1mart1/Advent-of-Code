
with open("in.txt") as f:
	arr = [int(l) for l in f.readlines()]

inc = 0
prev = arr[0]
for a in arr[1:]:
	inc += 1 if a > prev else 0
	prev = a
print("part1: number of larger meas than previous one: {}".format(inc))

inc = 0
prev = sum(arr[0:3])
for i in range(1, len(arr)-2):
	res = sum(arr[i:i+3])
	inc += 1 if res > prev else 0
	prev = res
print("part2: number of 3-meas larger meas than previous ones: {}".format(inc))
