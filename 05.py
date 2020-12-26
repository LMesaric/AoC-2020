with open("inputs/05.txt") as f:
    data = f.readlines()

seat_ids = set()
for line in data:
    binary_str = line.replace('F', '0').replace('B', '1').replace('L', '0').replace('R', '1')
    seat_ids.add(int(binary_str, base=2))

min_ = min(seat_ids)
max_ = max(seat_ids)
print("Max:", max_)

for i in range(min_, max_ + 1):
    if i not in seat_ids:
        print("Mine:", i)
        break
