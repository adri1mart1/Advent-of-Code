arr = []
size = 0

with open("in.txt") as f:
	for line in f:
		arr.append(line.rstrip())

print(arr)
size = len(arr[0])
print(size)
cnt_1s = [0] * size
final_res = [0] *size

print(cnt_1s)

for a in arr:
	for i in range(0, size):
		cnt_1s[i] += 1 if a[i] == '1' else 0

length = len(arr)

for i in range(0, size):
	if cnt_1s[i] > length/2:
		final_res[i] = 1
	else:
		final_res[i] = 0

print(cnt_1s)
print(f"len: {len(arr)}")
print(final_res)

str_final_res_int = ''.join(str(i) for i in final_res)
print(str_final_res_int)
res1 = int(str_final_res_int, 2)
print(res1)

str_revert = ""
for l in str_final_res_int:
	str_revert += '1' if l == '0' else '0'

print(str_revert)
res2 = int(str_revert, 2)
print(res2)

print("part 1: {}".format(res1 * res2))

arr_saved = arr

# find oxy gen rating
for i in range(0, size):
	cnt_1s = 0
	length = len(arr)
	print("rotation {}".format(0))
	for a in arr:
		print(a)
		cnt_1s += 1 if a[i] == '1' else 0

	print(cnt_1s)

	if cnt_1s >= length / 2:
		print("more ones, so keep ones")
		arr2 = []
		for a in arr:
			if a[i] == '1':
				arr2.append(a)
		arr = arr2
	else:
		print("more zeros, so keep zeros")
		arr2 = []
		for a in arr:
			if a[i] == '0':
				arr2.append(a)
		arr = arr2

oxygen = int(arr[0], 2)
print(oxygen)
print(arr)

print()
print()
print()

arr = arr_saved

# find CO2
for i in range(0, size):
	cnt_0s = 0
	length = len(arr)
	print("rotation {}".format(0))
	for a in arr:
		print(a)
		cnt_0s += 1 if a[i] == '0' else 0

	print(cnt_0s)

	if cnt_0s <= length / 2:
		print("less zeros, so keep zeros")
		arr2 = []
		for a in arr:
			if a[i] == '0':
				arr2.append(a)
		arr = arr2
	else:
		print("more zeros, so keep ones")
		arr2 = []
		for a in arr:
			if a[i] == '1':
				arr2.append(a)
		arr = arr2
	if len(arr) == 1:
		break

co2 = int(arr[0], 2)
print(co2)
print(arr)

print("part2: {}".format(oxygen*co2))
