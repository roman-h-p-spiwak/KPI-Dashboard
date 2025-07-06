from os import DirEntry, makedirs, path, scandir
from re import findall



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
            x = findall(r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) Report(?:_(?:[2-9]|(?:[1-9]+[0-9]+)))?\b Draft(?:_(?:[2-9]|(?:[1-9]+[0-9]+)))?\b", entry.name)
        case _:
            print(f"\033[0;31mError: Passed control variable `{control}` doesn't exist.\033[0m")
            return False
    print(f"\033[0;32m Success: Control variable `{control}` was properly passed.\033[0m")
    return len(x) == 1 and x[0] == entry.name

def year_create(directory: str, year: str) -> bool:
    year_folder = path.join(directory, year)
    if not directory_create(year_folder):
        return False
    ...
    return True

def report_create(directory: str, month: str) -> bool:
    month += " Report"
    month_folder = path.join(directory, month)
    if path.isdir(month_folder):
        month += "_"
        i = 2
        month_folder = path.join(directory, month + str(i))
        while path.isdir(month_folder) and i <= 99:
            i += 1
            month_folder = path.join(directory, month + str(i))
    
    if not directory_create(month_folder):
        return False
    ...
    return True
    
def directory_create(directory: str) -> bool:
    try:
        makedirs(directory, exist_ok=False)
        return True
    except FileExistsError:
        print(f"\033[0;31mError: The directory `{directory}` already exists.\033[0m")
        return False
    except Exception as e:
        print(f"\033[0;31mError: An unexpected error {e} occurred while attempting to create directory {directory}.\033[0m")
        return False

def main():
    year_create("./.testdata/", "2024-2025")
    year_create("./.testdata/", "2025-2026")
    report_create("./.testdata/", "Jan")
    report_create("./.testdata/", "Dec")
    report_create("./.testdata/", "Jan")
    report_create("./.testdata/", "Feb")
    print(year_index("./.testdata/"))
    print(report_index("./.testdata/"))
    print(draft_report_index("./.testdata/"))
    pass

main()