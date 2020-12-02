with open("inputs/2.txt") as f:
    data = f.readlines()

cnt1 = cnt2 = 0
for line in data:
    ranges, char, password = line.split()
    low, high = map(int, ranges.split('-'))
    char = char.strip(' :')
    password = password.strip()

    cnt1 += low <= password.count(char) <= high
    cnt2 += (password[low - 1] == char) ^ (password[high - 1] == char)

print(cnt1)
print(cnt2)
