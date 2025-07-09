

def read_csv(input: str, ) -> list:
    data = []
    with open(input, 'r') as file:
        i = 0
        for line in file:
            data.append([])
            entry = ""
            control = False
            for char in line: #TODO: Change to ignore last character on a line.
                if not control and char == ',':
                    data[i].append(entry)
                    entry = ""
                    continue
                if char == '(':
                    entry += char
                    control = True
                    continue
                if char ==')':
                    entry += char
                    control = False
                    data[i].append(entry)
                    entry = ""
                    continue
                entry += char
            i += 1
    return data
