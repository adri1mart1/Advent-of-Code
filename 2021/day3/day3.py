orig_arr, arr = [], []

# read input data saved into orig_array variable
with open("in.txt") as f:
	for line in f:
		orig_arr.append(line.rstrip())

# number of digit per line
digit_number = len(orig_arr[0])
# number of values in input data
length = len(orig_arr)

# table of N element to hold number of 1s over all array values per position
cnt_1s = [0] * digit_number
for a in orig_arr:
	for i in range(0, digit_number):
		cnt_1s[i] += 1 if a[i] == '1' else 0

# get the gamma rate
final_res = [0] * digit_number
for i in range(0, digit_number):
	final_res[i] = 1 if cnt_1s[i] > length/2 else 0

rs1 = ''.join(str(i) for i in final_res)
r1 = int(rs1, 2)

# get the epsilon rate
rs2 = ""
for l in rs1:
	rs2 += '1' if l == '0' else '0'
r2 = int(rs2, 2)

print("part 1: power consumption of the submarine: {}".format(r1 * r2))



# backup original values
arr = orig_arr

# find oxygen rating
for i in range(0, digit_number):
	cnt_1s = 0
	length = len(arr)
	for a in arr:
		cnt_1s += 1 if a[i] == '1' else 0

	if cnt_1s >= length / 2:
		arr2 = []
		for a in arr:
			if a[i] == '1':
				arr2.append(a)
		arr = arr2
	else:
		arr2 = []
		for a in arr:
			if a[i] == '0':
				arr2.append(a)
		arr = arr2
	if len(arr) == 1:
		break

oxygen = int(arr[0], 2)


# backup original values
arr = orig_arr

# find CO2 scrubber rate
for i in range(0, digit_number):
	cnt_0s = 0
	length = len(arr)
	for a in arr:
		cnt_0s += 1 if a[i] == '0' else 0

	if cnt_0s <= length / 2:
		arr2 = []
		for a in arr:
			if a[i] == '0':
				arr2.append(a)
		arr = arr2
	else:
		arr2 = []
		for a in arr:
			if a[i] == '1':
				arr2.append(a)
		arr = arr2
	if len(arr) == 1:
		break

co2 = int(arr[0], 2)


print("part 2: life support rating of the submarine: {}".format(oxygen*co2))
