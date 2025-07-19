from os import DirEntry, makedirs, path, scandir
from re import findall
from shutil import copy, copytree
from modules.inputs import helper, read_csv, create_csv, modify_cell, find_row
import modules.defaults as defaults



def get_app_configs(path_to_config: str, config_name: str = "configs.csv") -> list:
    
    data = read_csv(path_to_config, config_name)
    if not data:
        return create_app_configs(path_to_config, config_name)
    
    if not verify_app_configs(data):
        return create_app_configs(path_to_config, config_name)
    
    return data

def verify_app_configs(data: list) -> bool:
    home_directory_row = find_row(data, "home_directory")
    try:
        if home_directory_row == -1 or not path.exists(data[home_directory_row][1]):
            return False
        
        button_height_row = find_row(data, "button_height")
        if button_height_row == -1 or int(data[button_height_row][1]) <= 0:
            return False
        
        button_width_row = find_row(data, "button_width")
        if button_width_row == -1 or int(data[button_width_row][1]) <= 0:
            return False
        
        ... #TODO: Populate with all the possible config data and checks.
    except Exception as e:
        print(f"\033[0;31mError: The data is formatted incorrectly, resulting in {e}.\033[0m")
        return False
    return True

def create_app_configs(path_to_config: str, config_name: str = "configs.csv") -> list[list[str]]:
    if create_csv(path_to_config, config_name, defaults.APP_CONFIGS):
        home_directory_row = find_row(defaults.APP_CONFIGS, "home_directory")
        if not path.exists(defaults.APP_CONFIGS[home_directory_row][1]):
            makedirs(defaults.APP_CONFIGS[home_directory_row][1])
        return defaults.APP_CONFIGS
    return [[""]]

def year_index(directory: str) -> list[tuple]:
    return directory_index(directory, 0)

def report_index(directory: str) -> list[tuple]:
    #TODO: This should sort each report not alphabetically, but by the month (in the fiscal year).
    return directory_index(directory, 1)

def draft_report_index(directory: str) -> list[tuple]:
    return directory_index(directory, 2)

def directory_index(directory: str, control: int) -> list[tuple]:
    try:
        print(f"\033[0;32m Success: Accessed directory `{directory}` without error.\033[0m")
        return [(entry.path, entry.name) for entry in scandir(directory) if directory_check(entry, control)]
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

def year_create(directory: str, year: str, comp_year = "") -> bool:
    year_folder = path.join(directory, year)
    year_configs_folder = path.join(year_folder, "configs")
    year_inputs_folder = path.join(year_folder, "inputs")
    year_data_folder = path.join(year_inputs_folder, "data")
    year_targets_folder = path.join(year_inputs_folder, "targets")
    if (
        not directory_create(year_folder) or 
        not directory_create(year_configs_folder) or 
        not directory_create(year_inputs_folder) or 
        not directory_create(year_data_folder) or 
        not directory_create(year_targets_folder)
    ):
        return False
    
    if comp_year and comp_year != "None":
        comp_year_folder = path.join(directory, comp_year)
        if not path.isdir(comp_year_folder):
            print(f"\033[0;31mError: The year `{comp_year}` doesn't exist.\033[0m")
            return False
        comp_year_configs_folder = path.join(comp_year_folder, "configs")
        
        copy_or_create(comp_year_configs_folder, "goals.csv", year_configs_folder, "goals.csv", defaults.GOALS)
        copy_or_create(comp_year_configs_folder, "sub_goals.csv", year_configs_folder, "sub_goals.csv", defaults.SUB_GOALS)
        copy_or_create(comp_year_configs_folder, "data.csv", year_configs_folder, "data.csv", defaults.DATA)
    elif (
        not create_csv(year_configs_folder, "goals.csv", defaults.GOALS) or 
        not create_csv(year_configs_folder, "sub_goals.csv", defaults.SUB_GOALS) or 
        not create_csv(year_configs_folder, "data.csv", defaults.DATA)
    ):
        return False
    if not create_csv(year_configs_folder, "configs.csv", defaults.YEAR_CONFIGS):
        return False
    
    for row in read_csv(year_configs_folder, "data.csv")[1:]:
        data = helper(row[1])
        create_csv(year_data_folder, f"{row[0]}.csv", [data])
        
    for row in read_csv(year_configs_folder, "sub_goals.csv")[1:]:
        data = helper(row[3])
        data.insert(0, "date")
        create_csv(year_targets_folder, f"{row[0]}_targets.csv", [data])
    
    
    if not modify_cell(year_configs_folder, "configs.csv", comp_year, "comp_year", "value"):
        return False
    
    print(f"\033[0;32m Success: The directory for the year `{year}` was created without error.\033[0m")
    return True

def copy_or_create(source_path: str, source_name: str, destination_path: str, destination_name: str, data: list) -> bool:
    try:
        source = path.join(source_path, source_name)
        destination = path.join(destination_path, destination_name)
        copy(source, destination)
    except FileNotFoundError:
        print(f"\033[0;31mError: The file `{source}` doesn't exist. Using default instead.\033[0m")
        if not create_csv(destination_path, destination_name, data):
            return False
    except Exception as e:
        print(f"\033[0;31mError: An unexpected error {e} occurred while attempting to copy `{source}` to `{destination}`.\033[0m")
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
    
    month_inputs_folder = path.join(month_folder, "inputs")
    month_outputs_folder = path.join(month_folder, "outputs")
    month_graphs_folder = path.join(month_outputs_folder, "graphs")
    if (
        not directory_create(month_folder) or 
        not directory_create(month_inputs_folder) or 
        not directory_create(month_outputs_folder) or 
        not directory_create(month_graphs_folder)
    ):
        return False
    
    copytree(f"{directory}/inputs/data", f"{month_inputs_folder}/data")
    
    
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
