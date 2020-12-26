from math import prod

with open("inputs/03.txt") as f:
    data = [x.strip() for x in f.readlines()]

slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
cnts = [0] * len(slopes)

row_len = len(data[0])
row_num = len(data)

for i in range(len(slopes)):
    pos_down, pos_right = 0, 0

    while True:
        pos_down += slopes[i][1]
        if pos_down >= row_num:
            break
        pos_right = (pos_right + slopes[i][0]) % row_len
        cnts[i] += data[pos_down][pos_right] == '#'

print(cnts)
print(prod(cnts))
