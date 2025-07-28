from datetime import datetime
from os import DirEntry, path, rename, remove
from shutil import rmtree
from typing import Any

#TODO: Make sure all the success and error statements don't have leading whitespace.

def check_csv(path_to_file: str, name_of_file: str) -> bool:
    if not path.isfile(path.join(path_to_file, name_of_file)):
        print(f"\033[0;31mError: No such file `{name_of_file}` exists at `{path_to_file}`.\033[0m")
        return False
    return True

def helper(data_cell: str) -> list[str]: #TODO: If a line has a comma in it, it should be wrapped in quotation marks.
    data = data_cell.split(",")
    if len(data) > 1:
        data[0] = data[0][1:]
        data[-1] = data[-1][:-1]
    if data == ["()"]:
        return []
    return data

def read_csv(path_to_file: str, name_of_file: str) -> list[list[Any]]:
    if not check_csv(path_to_file, name_of_file):
        return []
    
    data = []
    with open(path.join(path_to_file, name_of_file) , 'r') as file:
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
            if entry != "\n":
                data[i].append(entry[:-1])
            i += 1
            
    print(f"\033[0;32m Success: The file `{name_of_file}` was read without error at `{path_to_file}`.\033[0m")
    return data

def write_csv(path_to_file: str, name_of_file: str, data: list[list[Any]]) -> bool:
    if not check_csv(path_to_file, name_of_file):
        return False
    
    with open(path.join(path_to_file, name_of_file), 'w') as file:
        for row in data:
            for column in row:
                file.write(column)
                file.write(',')
            file.write('\n')
        
    print(f"\033[0;32m Success: The file `{name_of_file}` at `{path_to_file}` was written without error.\033[0m")
    return True

def create_csv(path_to_file: str, name_of_file: str, data: list[list[Any]]) -> bool:
    if path.isfile(path.join(path_to_file, name_of_file)):
        name_of_old_file = f"obsolete_on_{datetime.today().strftime('%Y-%m-%d')}"
        num_str_ins = ""
        num = 2
        if path.isfile(path.join(path_to_file, f"{name_of_old_file}_{name_of_file}")):
            while num <= 99 and path.isfile(path.join(path_to_file, f"{name_of_old_file}_{num}_{name_of_file}")):
                num += 1
            if num == 100:
                print(f"\033[0;31mError: One-Hundred instances of `{name_of_old_file}_XX_{name_of_file}` already exist at `{path_to_file}`.\033[0m")
                return False
            num_str_ins = f"_{num}"
        name_of_old_file += f"{num_str_ins}_{name_of_file}"
        rename(path.join(path_to_file, name_of_file), path.join(path_to_file, name_of_old_file))
        print(f"\033[0;32m Success: The file `{name_of_file}` was renamed to `{name_of_old_file}` at `{path_to_file}` without error.\033[0m")
    
    #? Is this a waste of resources? Opening and closing the file just to make it, before opening and closing the file to write to it?
    with open(path.join(path_to_file, name_of_file), "w"):
        pass
    return write_csv(path_to_file, name_of_file, data)

def delete_csv(path_to_file: str):
    if path.isfile(path_to_file):
        remove(path_to_file)
        print(f"\033[0;32m Success: The file `{path_to_file}` was successfully deleted without error.\033[0m")
    elif path.isdir(path_to_file):
        rmtree(path_to_file)
        print(f"\033[0;32m Success: The folder `{path_to_file}` was successfully deleted without error.\033[0m")
    else:
        print(f"\033[0;31mError: The path `{path_to_file}` wasn't deleted as it doesn't exist.\033[0m")

def find_row(data: list[list], row: str) -> int:
    for i in range(len(data)):
        if data[i][0] == row:
            return i
    print(f"\033[0;31mError: The row `{row}` doesn't exist.\033[0m")
    return -1

def find_column(data: list, column: str) -> int:
    try:
        return data.index(column)
    except ValueError:
        print(f"\033[0;31mError: The column `{column}` doesn't exist.\033[0m")
        return -1

def modify_cell(path_to_file: str, name_of_file: str, new_data: str, row_name: str, column_name: str) -> bool:
    data = read_csv(path_to_file, name_of_file)
    if not data:
        return False
    row = find_row(data, row_name)
    column = find_column(data[0], column_name)
    if row == -1 or column == -1:
        return False
    data[row][column] = new_data
    return write_csv(path_to_file, name_of_file, data)


def find_graph_data(time: str, 
                    summed_column_cell: str, 
                    year_data_files: list[list[list[str]]], 
                    target_file: list[list[str]], 
                    comp_year_files: list[list[list[str]]], 
                    month: int) -> list[list[float]]:
    data = []
    summed = helper(summed_column_cell)
    data.append(find_graph_data_helper(time, summed, year_data_files, month))
    # data.append([float(row[1]) for row in target_file[1:]])
    data.append(find_graph_data_helper(time, [target_file[0][1]], [target_file], 6))
    
    data.append(find_graph_data_helper(time, summed, comp_year_files, month))
    return data

def find_graph_data_helper(time: str, summed: list[str], data_files: list[list[list[str]]], month: int) -> list[float]:
    if not data_files:
        return []
    year = [7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6]
    month_index = year.index(month)
    output = []
    for i in range(month_index + 1):
        output.append(0)
    for data in data_files:
        columns = []
        for column in summed:
            if column == "rows": 
                columns.append(column)
                continue
            c = find_column(data[0], column)
            if c != -1:
                columns.append(c)
        ending_row = 1
        for m in range(month_index + 1):
            starting_row = ending_row
            while ending_row < len(data) and int(data[ending_row][0].split("/")[0]) == year[m]:
                for c in columns:
                    if c == "rows":
                        output[m] += 1
                        continue
                    output[m] += float(data[ending_row][c])
                ending_row += 1    
    if time == "annual":
        for i in range(1, len(output)):
            output[i] += output[i - 1]
    # print(output)
    return output

def find_targets(time: str, targets: list[list[str]], month: int) -> tuple[float, float]:
    starting_row, ending_row = find_starting_row(targets, month)
    if starting_row == -1:
        print(f"\033[0;31mError: The target hasn't been initialized.\033[0m")
        return (0, 0)
    compared_value: float = float(targets[starting_row][1])
    displayed_valued: float = compared_value
    if time == "annual":
        displayed_valued = float(targets[-1][1])
    return (compared_value, displayed_valued)

def find_data_files(data_files_cell: str, path_to_data: str, affix: str = "") -> list[list[list[str]]]:
    data_files = helper(data_files_cell)
    data = []
    for file in data_files:
        data.append(read_csv(path_to_data, f"{file}{affix}.csv"))
    return data

def find_summed(time: str, summed_column_cell: str, data_files: list[list[list[str]]], month: int) -> float:
    sum: float = 0
    for data in data_files:
        start_at, end_at = find_starting_row(data, month)
        if time == "annual":
            start_at = 1
        elif start_at == -1:
            continue
        
        header = data[0]
        data = data[start_at:end_at]
        summed = helper(summed_column_cell)
        # print(data)
        for column in summed:
            if column == "rows":
                sum += len(data)
                continue
            c = find_column(header, column)
            if c != -1:
                for row in data:
                    sum += int(row[c])
    return float(sum)

def find_starting_row(data: list[list[str]], month: int) -> tuple[int, int]:
    starting_row = -1
    ending_row = len(data)
    for i in range(1, len(data)):
        date = data[i][0].split("/") #TODO: Remove splitting like this.
        if int(date[0]) == month and starting_row == -1:
            starting_row = i
        if (int(date[0]) > month or (month == 12 and int(date[0]) == 1)) and starting_row != -1:
            ending_row = i
            break
    return (starting_row, ending_row)

def find_or_create_data_files(path_to_file: str, name_of_file: str, directory: str) -> list[tuple[str, str]]:
    files: list[tuple[str, str]] = []
    data_file: list[list[str]] = read_csv(path_to_file, name_of_file)
    for row in data_file[1:]:
        if not check_csv(path_to_file, name_of_file): #? Checking the file that we've already read-in? This probably is supposed to be `check_csv(directory, f"{row[0]}.csv")`.
            create_csv(directory, f"{row[0]}.csv", [helper(row[1])])
        files.append((directory, f"{row[0]}.csv"))
    return files

def find_or_create_target_files(path_to_file: str, name_of_file: str, directory: str) -> list[tuple[str, str]]:
    files: list[tuple[str, str]] = []
    data_file: list[list[str]] = read_csv(path_to_file, name_of_file)
    for row in data_file[1:]:
        if not check_csv(path_to_file, name_of_file): #? Checking the file that we've already read-in? This probably is supposed to be `check_csv(directory, f"{row[0]}.csv")`.
            create_csv(directory, f"{row[0]}_targets.csv", [["date", row[1]]])
        files.append((directory, f"{row[0]}_targets.csv"))
    return files