

def read_csv(input: str) -> list:
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

def write_csv(input: str, data: list) -> bool:
    with open(input, 'w') as file:
        for row in data:
            for column in row:
                file.write(column)
                file.write(',')
            file.write('\n')
        
    return True

def modify_csv(input: str, new_data: str, row: int, column: int) -> bool:
    data = read_csv(input)
    data[row][column] = new_data
    write_csv(input, data)
    return True

def find_row(data: list[list], row: str) -> int:
    for i in range(len(data)):
        if data[i][0] == row:
            return i
    print(f"\033[0;31mError: The row {row} doesn't exist.\033[0m")
    return -1

def find_column(data: list[list], column: str) -> int:
    try:
        return data[0].index(column)
    except ValueError:
        print(f"\033[0;31mError: The column {column} doesn't exist.\033[0m")
        return -1
    