from os import DirEntry, makedirs, path, scandir, startfile
import sys
from pathlib import Path
from re import findall, IGNORECASE
from shutil import copy, copytree
from modules.inputs import helper, read_csv, create_csv, modify_cell, find_row
import modules.defaults as defaults
from typing import Any
from pathlib import Path
from weasyprint import HTML, CSS
from jinja2 import Environment, FileSystemLoader, select_autoescape
from subprocess import call
from platform import system
from modules.objects import Goal

MONTHS = {
    1: ("Jan", "January"),
    "Jan": (1, "January"),
    "January": (1, "Jan"),

    2: ("Feb", "February"),
    "Feb": (2, "February"),
    "February": (2, "Feb"),

    3: ("Mar", "March"),
    "Mar": (3, "March"),
    "March": (3, "Mar"),

    4: ("Apr", "April"),
    "Apr": (4, "April"),
    "April": (4, "Apr"),

    5: ("May", "May"),
    "May": (5, "May"),

    6: ("Jun", "June"),
    "Jun": (6, "June"),
    "June": (6, "Jun"),

    7: ("Jul", "July"),
    "Jul": (7, "July"),
    "July": (7, "Jul"),

    8: ("Aug", "August"),
    "Aug": (8, "August"),
    "August": (8, "Aug"),

    9: ("Sep", "September"),
    "Sep": (9, "September"),
    "September": (9, "Sep"),

    10: ("Oct", "October"),
    "Oct": (10, "October"),
    "October": (10, "Oct"),

    11: ("Nov", "November"),
    "Nov": (11, "November"),
    "November": (11, "Nov"),

    12: ("Dec", "December"),
    "Dec": (12, "December"),
    "December": (12, "Dec"),
}

def get_configs(path_to_report: str) -> list[list[str]]:
    path_to_configs = path.join(path_to_report, "configs")
    return read_csv(path_to_configs, "configs.csv")

def has_report_pdf_generated(path_to_report: str, affix: str = "") -> bool:
    
    configs = get_configs(path_to_report)
    month_abr = configs[find_row(configs, "month")][1]
    
    path_to_pdf: str = path.join(path_to_report, "outputs", "reports")
    print(path.join(path_to_pdf, f"{month_abr} Report{affix}.pdf"))
    return path.exists(path.join(path_to_pdf, f"{month_abr} Report{affix}.pdf"))

def new_report_version(path_to_report: str) -> str:
    
    path_to_configs = path.join(path_to_report, "configs")
    configs = read_csv(path_to_configs, "configs.csv")
    
    versions_list = helper(configs[find_row(configs, "versions")][1])
    new_version = int(versions_list[-1]) + 1
    versions_list.append(str(new_version))
    modify_cell(path_to_configs, "configs.csv", f"({','.join(versions_list)})", "versions", "value")
    
    path_to_data = path.join(path_to_report, "inputs", "data")
    
    for data_file in scandir(path_to_data):
        if data_file.is_file():
            name, ext = path.splitext(data_file.name)
            # print(name)
            copy(data_file.path, path.join(path_to_data, f"{name}_{new_version}{ext}"))
    
    return str(new_version)
    

def report_finalization(path_to_report: str):
    
    path_to_configs = path.join(path_to_report, "configs")
    configs = read_csv(path_to_configs, "configs.csv")
    path_to_year = configs[find_row(configs, "year_directory")][1]
    versions_list = helper(configs[find_row(configs, "versions")][1])
    
    if not versions_list:
        modify_cell(path_to_configs, "configs.csv", "1", "versions", "value")
        modify_cell(path_to_configs, "configs.csv", path_to_report, "access_directory", "value")
        
        path_to_year_data = path.join(path_to_year, "inputs", "data")
        path_to_report_data = path.join(path_to_report, "inputs", "data")
        path_to_year_targets = path.join(path_to_year, "inputs", "targets")
        path_to_report_targets = path.join(path_to_report, "inputs", "targets")
        
        path_to_year_configs = path.join(path_to_year, "configs")
        path_to_report_configs = path.join(path_to_report, "configs")
        
        year_goal_path = path.join(path_to_year_configs, "goals.csv")
        report_goal_path = path.join(path_to_report_configs, "goals.csv")
        year_sub_goal_path = path.join(path_to_year_configs, "sub_goals.csv")
        report_sub_goal_path = path.join(path_to_report_configs, "sub_goals.csv")
        year_data_path = path.join(path_to_year_configs, "data.csv")
        report_data_path = path.join(path_to_report_configs, "data.csv")
        
        goals = read_csv(path_to_year_configs, "goals.csv")
        for goal in goals[1:]:
            copy(path.join(path_to_year_configs, f"{goal[0]}_extras.txt"), path.join(path_to_report_configs, f"{goal[0]}_extras.txt"))
        copy(year_goal_path, report_goal_path)
        copy(year_sub_goal_path, report_sub_goal_path)
        copy(year_data_path, report_data_path)
        
        copytree(path_to_year_data, path_to_report_data, dirs_exist_ok=True)
        copytree(path_to_year_targets, path_to_report_targets, dirs_exist_ok=True)

# goals_sub_goals: list[tuple[list[Any], list[SubGoal]]]
def report_generation(path_to_report: str, report_name: str,  year: str, goals: list[Goal], affix: str = "") -> bool:
    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=select_autoescape()
    )
    template = env.get_template("index.html")

    for goal in goals:
        for sub_goal in goal.sub_goals:
            sub_goal.path_to_graph = resource_uri(sub_goal.path_to_graph)
    
    path_to_file = resource_path(path.join(path_to_report, "outputs", "reports"))
    file_path = resource_path(path.join(path_to_file, f"{report_name}{affix}.pdf"))
    HTML(string=template.render(
    year=year[1], 
    month=report_name.split(" ")[0], 
    goals=goals),
     base_url=Path(".").resolve()).write_pdf(
    file_path,
    stylesheets=[
        CSS(filename="static/style.css"),
        CSS(filename="static/bulma.css")
        ])
    
    if system() == 'Darwin':       # macOS
        call(('open', file_path))
    elif system() == 'Windows':    # Windows
        startfile(file_path)
    else:                          # linux variants
        call(('xdg-open', file_path))
    
    return True

def get_base_path():
    if getattr(sys, 'frozen', False):
        return path.dirname(sys.executable)
    else:
        return path.dirname(path.abspath(sys.argv[0]))

def resource_path(relative_path = ""):
    return path.join(get_base_path(), relative_path)

def resource_uri(path: str) -> str:
    return Path(resource_path(path)).resolve().as_uri()

def get_app_configs(path_to_config: str, config_name: str = "configs.csv") -> list:
    
    data = read_csv(path_to_config, config_name)
    if not data:
        return create_app_configs(path_to_config, config_name)
    
    if not verify_app_configs(data):
        return create_app_configs(path_to_config, config_name)
    
    return data

def verify_app_configs(data: list) -> bool:
    hex_code_pattern = r"^#?([a-f0-9]{6}|[a-f0-9]{3})$"
    
    try:
        home_directory_row = find_row(data, "home_directory")
        if home_directory_row == -1 or not path.exists(data[home_directory_row][1]):
            return False
        
        button_height_row = find_row(data, "button_height")
        if button_height_row == -1 or int(data[button_height_row][1]) <= 0:
            return False
        
        button_width_row = find_row(data, "button_width")
        if button_width_row == -1 or int(data[button_width_row][1]) <= 0:
            return False
        
        comp_year_color = find_row(data, "comp_year_color")
        if comp_year_color == -1 or not findall(hex_code_pattern, data[comp_year_color][1], flags=IGNORECASE):
            return False
        
        target_color = find_row(data, "target_color")
        if target_color == -1 or not findall(hex_code_pattern, data[target_color][1], flags=IGNORECASE):
            return False
        
        year_color = find_row(data, "year_color")
        if year_color == -1 or not findall(hex_code_pattern, data[year_color][1], flags=IGNORECASE):
            return False
        
        ... #TODO: Populate with all the possible config data and checks.
        
    except Exception as e:
        print(f"\033[0;31mError: The data is formatted incorrectly, resulting in {e}.\033[0m")
        return False
    return True

def create_app_configs(path_to_config: str, config_name: str = "configs.csv") -> list[list[str]]:
    default_app_configs = defaults.APP_CONFIGS()
    if create_csv(path_to_config, config_name, default_app_configs):
        home_directory_row = find_row(default_app_configs, "home_directory")
        if not path.exists(default_app_configs[home_directory_row][1]):
            makedirs(default_app_configs[home_directory_row][1])
        return default_app_configs
    return [[""]]

def year_index(directory: str) -> list[tuple]:
    return directory_index(directory, 0)

def report_index(directory: str) -> list[tuple]:
    
    reports = directory_index(directory, 1)
    if not reports:
        return reports
    sorted_reports = []
    for i in range(12):
        sorted_reports.append(())
        
    for report in reports:
        match report[1]:
            case "Jul Report":
                sorted_reports[11] = report
            case "Aug Report":
                sorted_reports[10] = report
            case "Sep Report":
                sorted_reports[9] = report
            case "Oct Report":
                sorted_reports[8] = report
            case "Nov Report":
                sorted_reports[7] = report
            case "Dec Report":
                sorted_reports[6] = report
            case "Jan Report":
                sorted_reports[5] = report
            case "Feb Report":
                sorted_reports[4] = report 
            case "Mar Report":
                sorted_reports[3] = report
            case "Apr Report":
                sorted_reports[2] = report
            case "May Report":
                sorted_reports[1] = report
            case "Jun Report":
                sorted_reports[0] = report
            case _:
                print(f"\033[0;31mError: The report `{report}` does not exist.\033[0m")
    output = []
    for report in sorted_reports:
        if report != ():
            output.append(report)
    return output

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
            # x = findall(r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) Report(?:_(?:[2-9]|(?:[1-9]+[0-9]+)))?\b", entry.name)
            x = findall(r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) Report\b", entry.name) #! Obsolete.
        case 2:
            x = findall(r"[0-9]{4}-[0-9]{4} \b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) Report(?:_(?:[2-9]|(?:[1-9]+[0-9]+)))?\b Draft(?:_(?:[2-9]|(?:[1-9]+[0-9]+)))?\b", entry.name) #! Obsolete.
        case _:
            print(f"\033[0;31mError: Passed control variable `{control}` doesn't exist.\033[0m")
            return False
    print(f"\033[0;32m Success: Control variable `{control}` was properly passed.\033[0m")
    return len(x) == 1 and x[0] == entry.name

def year_create(home_directory: str, year: str, comp_year = "") -> bool:
    year_folder = path.join(home_directory, year)
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
    
    # if comp_year and comp_year != "None":
    #     comp_year_folder = path.join(home_directory, comp_year)
    #     if not path.isdir(comp_year_folder):
    #         print(f"\033[0;31mError: The year `{comp_year}` doesn't exist.\033[0m")
    #         return False
    #     comp_year_configs_folder = path.join(comp_year_folder, "configs")
        
    #     copy_or_create(comp_year_configs_folder, "goals.csv", year_configs_folder, "goals.csv", defaults.GOALS)
    #     copy_or_create(comp_year_configs_folder, "sub_goals.csv", year_configs_folder, "sub_goals.csv", defaults.SUB_GOALS)
    #     copy_or_create(comp_year_configs_folder, "data.csv", year_configs_folder, "data.csv", defaults.DATA)
    # el
    if (
        not create_csv(year_configs_folder, "goals.csv", defaults.GOALS(int(year.split("-")[1]))) or 
        not create_csv(year_configs_folder, "sub_goals.csv", defaults.SUB_GOALS(int(year.split("-")[1]))) or 
        not create_csv(year_configs_folder, "data.csv", defaults.DATA())
    ):
        return False
    if not create_csv(year_configs_folder, "configs.csv", defaults.YEAR_CONFIGS(year, comp_year)):
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

def year_next_year_insert(path_to_file: str, name_of_file: str, year: int):
    pass

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
    

def report_create(year_directory: str, month: str) -> bool:
    month_folder = path.join(year_directory, f"{month} Report")
    if path.isdir(month_folder):
        # num = 2
        # while num <= 99 and path.isdir(f"{month_folder}_{num}"):
        #     num += 1
        # if num == 100:
        #     print(f"\033[0;31mError: One-Hundred instances of `{month} Report` already exist.\033[0m")
        #     return False
        # month_folder = path.join(year_directory, f"{month} Report_{num}")
        print(f"\033[0;31mError: The report `{month} Report` already exist.\033[0m")
        return False #TODO: The function that called this should display the error message to the user.
    
    month_configs_folder = path.join(month_folder, "configs")
    month_inputs_folder = path.join(month_folder, "inputs")
    month_data_folder = path.join(month_inputs_folder, "data")
    month_targets_folder = path.join(month_inputs_folder, "targets")
    month_outputs_folder = path.join(month_folder, "outputs")
    month_graphs_folder = path.join(month_outputs_folder, "graphs")
    month_reports_folder = path.join(month_outputs_folder, "reports")
    if (
        not directory_create(month_folder) or 
        not directory_create(month_configs_folder) or 
        not directory_create(month_inputs_folder) or 
        not directory_create(month_data_folder) or 
        not directory_create(month_targets_folder) or 
        not directory_create(month_outputs_folder) or 
        not directory_create(month_graphs_folder) or 
        not directory_create(month_reports_folder)
    ):
        return False
    
    create_csv(month_configs_folder, "configs.csv", defaults.MONTH_CONFIGS(year_directory, month))
    
    # copy_or_create(path.join(directory, "configs"), "data.csv", month_configs_folder, "data.csv", defaults.DATA)
    # copy_or_create(path.join(directory, "configs"), "goals.csv", month_configs_folder, "goals.csv", defaults.GOALS)
    # copy_or_create(path.join(directory, "configs"), "sub_goals.csv", month_configs_folder, "sub_goals.csv", defaults.SUB_GOALS)
    
    # copytree(path.join(directory, "inputs", "data"), path.join(month_inputs_folder, "data"))
    
    
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
