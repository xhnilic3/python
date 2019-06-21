import string
import sys

with open(sys.argv[1]) as f:
    rows = [line.rstrip('\n') for line in f]


for row in rows:
    if (int(row.split()[6].replace("%", "")) > int(sys.argv[2])):
        print(row.split()[0].replace(":", ""))	


