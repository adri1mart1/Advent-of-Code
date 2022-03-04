
csvlist = []
baselist = []

with open("meli-csv-noport.txt") as f:
	for line in f:
		csvlist.append(line.rstrip())


with open("meli-base-noport.txt") as f:
	for line in f:
		baselist.append(line.rstrip())

print(csvlist)
