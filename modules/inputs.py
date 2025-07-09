

def read_csv(input: str, ) -> list:
    data = []
    with open(input, 'r') as file:
        i = 0
        for line in file:
            data.append([])
            entry = ""
            control = False
            for char in line:
                if char == '(':
                    entry += char
                    control = True
                    continue
                if char ==')':
                    entry += char
                    control = False
                    continue
                if not control and char == ',':
                    data[i].append(entry)
                    entry = ""
                    continue
                entry += char
            i += 1
    return data


i = read_csv("default_sub_goals.csv")
for j in i:
    for k in j:
        print(k, end=" | ")
    print()
# print()
# print()
# print()
# print()
# print(read_csv("default_sub_goals.csv"))
