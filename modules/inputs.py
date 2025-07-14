from datetime import datetime
from os import DirEntry, path, rename

#TODO: Make sure all the success and error statements don't have leading whitespace.

def check_csv(path_to_file: str) -> bool:
    if not path.isfile(path_to_file):
        print(f"\033[0;31mError: No such file `{path_to_file}` exists.\033[0m")
        return False
    return True

def read_csv(path_to_file: str) -> list:
    if not check_csv(path_to_file):
        return []
    
    data = []
    with open(path_to_file , 'r') as file:
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
    print(f"\033[0;32m Success: The file `{path_to_file}` was read without error.\033[0m")
    return data

def write_csv(path_to_file: str, data: list) -> bool:
    if not check_csv(path_to_file):
        return False
    
    with open(path_to_file, 'w') as file:
        for row in data:
            for column in row:
                file.write(column)
                file.write(',')
            file.write('\n')
        
    print(f"\033[0;32m Success: The file `{path_to_file}` was written without error.\033[0m")
    return True

def create_csv(path_to_file: str, data: list) -> bool:
    if path.isfile(path_to_file):
        path_to_old_file = f"obsolete_on_{datetime.today().strftime('%Y-%m-%d')}_{path_to_file}"
        num = 2
        if path.isfile(path_to_old_file):
            while num <= 99 and path.isfile(f"{path_to_old_file}_{num}"):
                num += 1
            if num == 100:
                print(f"\033[0;31mError: One-Hundred instances of `{path_to_old_file}` already exist.\033[0m")
                return False
            path_to_old_file += f"_{num}"
        rename(path_to_file, f"{path_to_old_file}")
        print(f"\033[0;32m Success: The file `{path_to_file}` was renamed to `{path_to_old_file}` without error.\033[0m")
    
    #? Is this a waste of resources? Opening and closing the file just to make it, before opening and closing the file to write to it?
    with open(path_to_file, "w"):
        pass
    return write_csv(path_to_file, data)

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

def modify_cell(path_to_file: str, new_data: str, row_name: str, column_name: str) -> bool:
    data = read_csv(path_to_file)
    if not data:
        return False
    row = find_row(data, row_name)
    column = find_column(data, column_name)
    if row == -1 or column == -1:
        return False
    data[row][column] = new_data
    return write_csv(path_to_file, data)