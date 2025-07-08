from datetime import datetime
from os import DirEntry, makedirs, path, rename, scandir
from re import findall
import inputs as inputs



DEFAULT_SUB_GOALS = ""



def year_index(directory: str) -> list[tuple]:
    return directory_index(directory, 0)

def report_index(directory: str) -> list[tuple]:
    return directory_index(directory, 1)

def draft_report_index(directory: str) -> list[tuple]:
    return directory_index(directory, 2)

def directory_index(directory: str, control: int) -> list[tuple]:
    try:
        print(f"\033[0;32m Success: Accessed directory `{directory}` without error.\033[0m")
        return [(entry.name, entry.path) for entry in scandir(directory) if directory_check(entry, control)]
    except FileNotFoundError:
        print(f"\033[0;31mError: The directory `{directory}` does not exist.\033[0m")
        return [()]
    except PermissionError:
        print(f"\033[0;31mError: Permission denied to access `{directory}`.\033[0m")
        return [()]

def directory_check(entry: DirEntry, control: int) -> bool:
    if not entry.is_dir():
        return False
    match control:
        case 0:
            x = findall("[0-9]{4}-[0-9]{4}", entry.name)
        case 1:
            x = findall(r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) Report(?:_(?:[2-9]|(?:[1-9]+[0-9]+)))?\b", entry.name)
        case 2:
            x = findall(r"[0-9]{4}-[0-9]{4} \b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) Report(?:_(?:[2-9]|(?:[1-9]+[0-9]+)))?\b Draft(?:_(?:[2-9]|(?:[1-9]+[0-9]+)))?\b", entry.name)
        case _:
            print(f"\033[0;31mError: Passed control variable `{control}` doesn't exist.\033[0m")
            return False
    print(f"\033[0;32m Success: Control variable `{control}` was properly passed.\033[0m")
    return len(x) == 1 and x[0] == entry.name

def year_create(directory: str, year: str) -> bool:
    year_folder = path.join(directory, year)
    year_data_folder = path.join(year_folder, "Data")
    year_targets_folder = path.join(year_data_folder, "Targets")
    year_annual_goals_folder = path.join(year_data_folder, "Annual Goals")
    if (
        not directory_create(year_folder) and 
        not directory_create(year_data_folder) and 
        not directory_create(year_targets_folder) and
        not directory_create(year_annual_goals_folder)
    ):
        return False
    
    
    return True

def report_create(directory: str, month: str) -> bool:
    month_folder = path.join(directory, f"{month} Report")
    if path.isdir(month_folder):
        num = 2
        while num <= 99 and path.isdir(f"{month_folder}_{num}"):
            num += 1
        if num == 100:
            print(f"\033[0;31mError: One-Hundred instances of `{month} Report` already exist.\033[0m")
            return False
        month_folder = path.join(directory, f"{month} Report_{num}")
    
    month_data_folder = path.join(month_folder, "Data")
    month_outputs_folder = path.join(month_folder, "Outputs")
    if (
        not directory_create(month_folder) and 
        not directory_create(month_data_folder) and 
        not directory_create(month_outputs_folder)
    ):
        return False
    ...
    
    return True
    
def directory_create(directory: str) -> bool:
    try:
        makedirs(directory, exist_ok=False)
        print(f"\033[0;32m Success: The directory `{directory}` was created without error.\033[0m")
        return True
    except FileExistsError:
        print(f"\033[0;31mError: The directory `{directory}` already exists.\033[0m")
        return False
    except Exception as e:
        print(f"\033[0;31mError: An unexpected error {e} occurred while attempting to create directory {directory}.\033[0m")
        return False


def file_create(directory: str, file_name: str, default_content: str) -> bool:
    path_to_file = path.join(directory, file_name)
    if path.isfile(path_to_file):
        old_file = f"{file_name}_obsolete_on_{datetime.today().strftime('%Y-%m-%d')}"
        path_to_old_file = path.join(directory, old_file)
        num = 2
        if path.isfile(path_to_old_file):
            while num <= 99 and path.isfile(f"{path_to_old_file}_{num}"):
                num += 1
            if num == 100:
                print(f"\033[0;31mError: One-Hundred instances of `{old_file}` already exist.\033[0m")
                return False
            path_to_old_file += f"_{num}"
            old_file += f"_{num}"
        rename(path_to_file, f"{path_to_old_file}")
        print(f"\033[0;32m Success: The file `{file_name}` was renamed to `{old_file}` without error.\033[0m")
    
    with open(path_to_file, "w") as file:
        file.write(default_content)
    print(f"\033[0;32m Success: The file `{file_name}` had the content `{default_content}` written without error.\033[0m")
    
    return True

file_create("./", "test.csv", "sub_goal, data_file, monthly, summed_column, (stuff, stuff1, stuff2, stuff3)")
print(inputs.read_csv("./test.csv"))