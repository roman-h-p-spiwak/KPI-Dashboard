from datetime import datetime
from os import DirEntry, path, rename, remove
from shutil import rmtree
from typing import Any
# from modules.objects import log

#TODO: Make sure all the success and error statements don't have leading whitespace.

def check_csv(path_to_file: str, 
              name_of_file: str, 
              error_code: str = "") -> bool:
    error_code += "0"
    if not path.isfile(path.join(path_to_file, name_of_file)):
        print(f"\033[0;31mError {error_code}: No such file `{name_of_file}` exists at `{path_to_file}`.\033[0m")
        log(f"\033[0;31mError {error_code}: No such file `{name_of_file}` exists at `{path_to_file}`.\033[0m")
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

def read_csv(path_to_file: str, 
             name_of_file: str, 
             error_code: str = "") -> list[list[Any]]:
    error_code += "1"
    if not check_csv(path_to_file, name_of_file, error_code=f"{error_code}_"):
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
            
    print(f"\033[0;32mSuccess: The file `{name_of_file}` was read without error at `{path_to_file}`.\033[0m")
    log(f"\033[0;32mSuccess: The file `{name_of_file}` was read without error at `{path_to_file}`.\033[0m")
    return data

def write_csv(path_to_file: str, 
              name_of_file: str, 
              data: list[list[Any]], 
              error_code: str ="") -> bool:
    error_code += "2"
    if not check_csv(path_to_file, name_of_file, error_code=f"{error_code}_"):
        return False
    
    with open(path.join(path_to_file, name_of_file), 'w') as file:
        for row in data:
            for column in row:
                file.write(column)
                file.write(',')
            file.write('\n')
        
    print(f"\033[0;32mSuccess: The file `{name_of_file}` at `{path_to_file}` was written without error.\033[0m")
    log(f"\033[0;32mSuccess: The file `{name_of_file}` at `{path_to_file}` was written without error.\033[0m")
    return True

def create_csv(path_to_file: str, 
               name_of_file: str, 
               data: list[list[Any]], 
               error_code: str ="") -> bool:
    error_code += "3"
    if create_file(path_to_file, name_of_file, error_code=f"{error_code}_"):
        return write_csv(path_to_file, name_of_file, data, error_code=f"{error_code}_")
    else:
        return False

def create_file(path_to_file: str, 
                name_of_file: str, 
                data: list[list[Any]] = [], 
                error_code: str = "") -> bool:
    error_code += "4"
    if check_csv(path_to_file, name_of_file, error_code=f"{error_code}_"):
        name_of_old_file = f"obsolete_on_{datetime.today().strftime('%Y-%m-%d')}"
        num_str_ins = ""
        num = 2
        if path.isfile(path.join(path_to_file, f"{name_of_old_file}_{name_of_file}")):
            while num <= 99 and path.isfile(path.join(path_to_file, f"{name_of_old_file}_{num}_{name_of_file}")):
                num += 1
            if num == 100:
                print(f"\033[0;31mError: One-Hundred instances of `{name_of_old_file}_XX_{name_of_file}` already exist at `{path_to_file}`.\033[0m")
                log(f"\033[0;31mError: One-Hundred instances of `{name_of_old_file}_XX_{name_of_file}` already exist at `{path_to_file}`.\033[0m")
                return False
            num_str_ins = f"_{num}"
        name_of_old_file += f"{num_str_ins}_{name_of_file}"
        rename(path.join(path_to_file, name_of_file), path.join(path_to_file, name_of_old_file))
        print(f"\033[0;32mSuccess: The file `{name_of_file}` was renamed to `{name_of_old_file}` at `{path_to_file}` without error.\033[0m")
        log(f"\033[0;32mSuccess: The file `{name_of_file}` was renamed to `{name_of_old_file}` at `{path_to_file}` without error.\033[0m")
        log(f"\033[0;32mSuccess: The file `{name_of_file}` was renamed to `{name_of_old_file}` at `{path_to_file}` without error.\033[0m")
    
    #? Is this a waste of resources? Opening and closing the file just to make it, before opening and closing the file to write to it?
    with open(path.join(path_to_file, name_of_file), "w") as file:
        if not data:
            for row in data:
                for column in row:
                    file.write(column)
                file.write("\n")
    return True

def delete_csv(path_to_file: str, error_code: str =""):
    error_code += "5"
    if path.isfile(path_to_file):
        remove(path_to_file)
        print(f"\033[0;32mSuccess: The file `{path_to_file}` was successfully deleted without error.\033[0m")
        log(f"\033[0;32mSuccess: The file `{path_to_file}` was successfully deleted without error.\033[0m")
    elif path.isdir(path_to_file):
        rmtree(path_to_file)
        print(f"\033[0;32mSuccess: The folder `{path_to_file}` was successfully deleted without error.\033[0m")
        log(f"\033[0;32mSuccess: The folder `{path_to_file}` was successfully deleted without error.\033[0m")
    else:
        print(f"\033[0;31mError {error_code}: The path `{path_to_file}` wasn't deleted as it doesn't exist.\033[0m")
        log(f"\033[0;31mError {error_code}: The path `{path_to_file}` wasn't deleted as it doesn't exist.\033[0m")

def find_row(data: list[list], row: str, error_code: str = "") -> int:
    error_code += "6"
    for i in range(len(data)):
        if data[i][0] == row:
            return i
    print(f"\033[0;31mError {error_code}: The row `{row}` doesn't exist.\033[0m")
    log(f"\033[0;31mError {error_code}: The row `{row}` doesn't exist.\033[0m")
    return -1

def find_column(data: list, column: str, error_code: str = "") -> int:
    error_code += "7"
    try:
        return data.index(column)
    except ValueError:
        print(f"\033[0;31mError {error_code}: The column `{column}` doesn't exist.\033[0m")
        log(f"\033[0;31mError {error_code}: The column `{column}` doesn't exist.\033[0m")
        return -1

def modify_cell(path_to_file: str, 
                name_of_file: str, 
                new_data: str, 
                row_name: str, 
                column_name: str, 
                error_code: str ="") -> bool:
    error_code += "8"
    data = read_csv(path_to_file, name_of_file, error_code=f"{error_code}_")
    if not data:
        return False
    row = find_row(data, row_name, error_code=f"{error_code}_")
    column = find_column(data[0], column_name, error_code=f"{error_code}_")
    if row == -1 or column == -1:
        return False
    data[row][column] = new_data
    return write_csv(path_to_file, name_of_file, data, error_code=f"{error_code}_")


def find_graph_data(time: str, 
                    summed_column_cell: str, 
                    year_data_files: list[list[list[str]]], 
                    target_file: list[list[str]], 
                    comp_year_files: list[list[list[str]]], 
                    month: int, 
                    error_code: str = "") -> list[list[float]]:
    error_code += "9"
    data = []
    summed = helper(summed_column_cell)
    data.append(find_graph_data_helper(time, summed, year_data_files, month, error_code=f"{error_code}_"))
    data.append(find_graph_data_helper(time, [target_file[0][1]], [target_file], 6, error_code=f"{error_code}_"))
    data.append(find_graph_data_helper(time, summed, comp_year_files, month, error_code=f"{error_code}_"))
    return data

def find_graph_data_helper(time: str, 
                           summed: list[str], 
                           data_files: list[list[list[str]]], 
                           month: int, 
                           error_code: str = "") -> list[float]:
    error_code += "10"
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
            c = find_column(data[0], column, error_code=f"{error_code}_")
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
    return output

def find_targets(time: str, 
                 targets: list[list[str]], 
                 month: int, 
                 error_code: str = "") -> tuple[float, float]:
    error_code += "11"
    starting_row, ending_row = find_starting_row(targets, month, error_code=f"{error_code}_")
    if starting_row == -1:
        print(f"\033[0;31mError {error_code}: The target hasn't been initialized.\033[0m")
        log(f"\033[0;31mError {error_code}: The target hasn't been initialized.\033[0m")
        return (0, 0)
    compared_value: float = float(targets[starting_row][1])
    displayed_valued: float = compared_value
    if time == "annual":
        displayed_valued = float(targets[-1][1])
    return (compared_value, displayed_valued)

def find_data_files(data_files_cell: str, 
                    path_to_data: str, 
                    affix: str = "", 
                    error_code: str = "") -> list[list[list[str]]]:
    error_code += "12"
    data_files = helper(data_files_cell)
    data = []
    for file in data_files:
        data.append(read_csv(path_to_data, f"{file}{affix}.csv", error_code=f"{error_code}_"))
    return data

def find_summed(time: str, 
                summed_column_cell: str, 
                data_files: list[list[list[str]]], 
                month: int, 
                error_code: str = "") -> float:
    error_code += "13"
    sum: float = 0
    for data in data_files:
        start_at, end_at = find_starting_row(data, month, error_code=f"{error_code}_")
        if time == "annual":
            start_at = 1
        elif start_at == -1:
            continue
        header = data[0]
        data = data[start_at:end_at]
        summed = helper(summed_column_cell)
        for column in summed:
            if column == "rows":
                sum += len(data)
                continue
            c = find_column(header, column, error_code=f"{error_code}_")
            if c != -1:
                for row in data:
                    sum += int(row[c])
    return float(sum)

def find_starting_row(data: list[list[str]], 
                      month: int, 
                      error_code: str = "") -> tuple[int, int]:
    error_code += "14"
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

def find_or_create_data_files(path_to_file: str, 
                              name_of_file: str, 
                              directory: str, 
                              error_code: str = "") -> list[tuple[str, str]]:
    error_code += "15"
    files: list[tuple[str, str]] = []
    data_file: list[list[str]] = read_csv(path_to_file, name_of_file, error_code=f"{error_code}_")
    for row in data_file[1:]:
        if not check_csv(directory, f"{row[0]}.csv", error_code=f"{error_code}_"):
            create_csv(directory, f"{row[0]}.csv", [helper(row[1])], error_code=f"{error_code}_")
        files.append((directory, f"{row[0]}.csv"))
    return files

def find_or_create_target_files(path_to_file: str, 
                                name_of_file: str, 
                                directory: str, 
                                error_code: str = "find_or_create_target_files") -> list[tuple[str, str]]:
    error_code += "16"
    files: list[tuple[str, str]] = []
    data_file: list[list[str]] = read_csv(path_to_file, name_of_file, error_code=f"{error_code}_")
    for row in data_file[1:]:
        if not check_csv(directory, f"{row[0]}.csv", error_code=f"{error_code}_"):
            create_csv(directory, f"{row[0]}_targets.csv", [["date", row[1]]], error_code=f"{error_code}_")
        files.append((directory, f"{row[0]}_targets.csv"))
    return files
def log(log: str):
    pass