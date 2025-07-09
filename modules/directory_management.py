from datetime import datetime
from os import DirEntry, makedirs, path, rename, scandir
from re import findall
from shutil import copy
from inputs import read_csv


DEFAULT_YEAR_CONFIGS = ""

DEFAULT_GOALS = """goal,percentage,(sub_goal_zero,sub_goal_one,sub_goal_two,...),
Value Proposition & Visibility,.5,(Marketing Messages,Community Events,EXP {next_year} Nominations,EXP {next_year} Applications,EXP {next_year} Enrollment,Leap {year} Nominations,Leap {year} Applications,Leap {year} Enrollment),
Community Engagement,.5,(LSM Lectures,Lecture Attendance,Calvert Attendance,Charles Attendance,St. Mary's Attendance,Satisfied/Very Satisfied,Interest Surveys),
Revenue,.5,(Fundraising Event Revenue,LSMAA Membership,LSMAA Revenue,Program Sponsors,LSM Lunch Sponsors,LSM Event Sponsors,Sponsorship Revenue),
"""

DEFAULT_SUB_GOALS = """sub_goal,data_file,storage,time,summed_column,committee,
Marketing Messages,marketing_messages,report,monthly,messages,communications,
Community Events,community_events,year,monthly,rows,communications,
EXP {next_year} Nominations,exp_nominations,year,annual,nominations,recruiting,
EXP {next_year} Applications,exp_applications,year,annual,applications,recruiting,
EXP {next_year} Enrollment,exp_enrollment,year,annual,enrollment,recruiting,
Leap {year} Nominations,leap_nominations,year,annual,nominations,leap/recruiting,
Leap {year} Applications,leap_applications,year,annual,applications,leap/recruiting,
Leap {year} Enrollment,leap_enrollment,year,annual,enrollment,leap/recruiting,
LSM Lectures,lectures,year,annual,rows,alumni,
Lecture Attendance,lectures,year,annual,(calvert,charles,st_mary),alumni,
Calvert Attendance,lectures,year,annual,calvert,alumni,
Charles Attendance,lectures,year,annual,charles,alumni,
St. Mary's Attendance,lectures,year,annual,st_mary,alumni,
Satisfied/Very Satisfied,lectures,year,annual,satisfaction,alumni,
Interest Surveys,surveys,year,annual,surveys,alumni/program,
Fundraising Event Revenue,fundraising,year,annual,revenue,development,
LSMAA Membership,lsmaa,year,annual,enrollment,alumni,
LSMAA Revenue,lsmaa,year,annual,revenue,alumni,
Program Sponsors,program_sponsors,year,annual,rows,development,
LSM Lunch Sponsors,lunch_sponsors,year,annual,rows,program,
LSM Event Sponsors,event_sponsors,year,annual,rows,development,
Sponsorship Revenue,(program_sponsors,lunch_sponsors,event_sponsors),year,annual,revenue,development,
"""

DEFAULT_DATA = """data_file_name,(data_column_zero,data_column_one,data_column_two,...),
marketing_messages,(source,messages),
community_events,(date,event_name,attendees),
exp_nominations,(month,nominations),
exp_applications,(month,applications),
exp_enrollment,(month,enrollment),
leap_nominations,(month,nominations),
leap_applications,(month,applications),
leap_enrollment,(month,enrollment),
lectures,(title,date,calvert,charles,st_mary,satisfaction),
surveys,(month,surveys),
fundraising,(date,event,source,revenue),
lsmaa,(month,enrollment,revenue),
program_sponsors,(date,sponsor,number,level,revenue,notes),
lunch_sponsors,(date,sponsor,session,pledged_paid,revenue,notes).
event_sponsors,(date,sponsor,event,revenue,notes),
"""



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

def year_create(directory: str, year: str, comp_year = None) -> bool:
    year_folder = path.join(directory, year)
    year_configs_folder = path.join(year_folder, "Configs")
    year_data_folder = path.join(year_folder, "Data")
    year_targets_folder = path.join(year_data_folder, "Targets")
    year_annual_goals_folder = path.join(year_data_folder, "Annual Goals")
    if (
        not directory_create(year_folder) or 
        not directory_create(year_configs_folder) or 
        not directory_create(year_data_folder) or 
        not directory_create(year_targets_folder) or 
        not directory_create(year_annual_goals_folder)
    ):
        return False
    
    if comp_year:
        comp_year_folder = path.join(directory, comp_year)
        if not path.isdir(comp_year_folder):
            print(f"\033[0;31mError: The year `{comp_year}` doesn't exist.\033[0m")
            return False
        comp_year_configs_folder = path.join(comp_year_folder, "Configs")
        # TODO: Clean up. This looks awful.
        try:
            copy(path.join(comp_year_configs_folder, "goals.csv"), path.join(year_configs_folder, "goals.csv"))
        except FileNotFoundError:
            print(f"\033[0;31mError: The `{comp_year}` `goals.csv` doesn't exist. Using default instead.\033[0m")
            if not file_create(year_configs_folder, "goals.csv", DEFAULT_GOALS):
                return False
        except Exception as e:
            print(f"\033[0;31mError: An unexpected error {e} occurred while attempting to copy `goals.csv` from {comp_year_configs_folder}.\033[0m")
            return False
        try:
            copy(path.join(comp_year_configs_folder, "sub_goals.csv"), path.join(year_configs_folder, "sub_goals.csv"))
        except FileNotFoundError:
            print(f"\033[0;31mError: The `{comp_year}` `sub_goals.csv` doesn't exist. Using default instead.\033[0m")
            if not file_create(year_configs_folder, "sub_goals.csv", DEFAULT_SUB_GOALS):
                return False
        except Exception as e:
            print(f"\033[0;31mError: An unexpected error {e} occurred while attempting to copy `sub_goals.csv` from {comp_year_configs_folder}.\033[0m")
            return False
        try:
            copy(path.join(comp_year_configs_folder, "data.csv"), path.join(year_configs_folder, "data.csv"))
        except FileNotFoundError:
            print(f"\033[0;31mError: The `{comp_year}` `data.csv` doesn't exist. Using default instead.\033[0m")
            if not file_create(year_configs_folder, "data.csv", DEFAULT_DATA):
                return False
        except Exception as e:
            print(f"\033[0;31mError: An unexpected error {e} occurred while attempting to copy `data.csv` from {comp_year_configs_folder}.\033[0m")
            return False
    elif (
        not file_create(year_configs_folder, "goals.csv", DEFAULT_GOALS) or 
        not file_create(year_configs_folder, "sub_goals.csv", DEFAULT_SUB_GOALS) or 
        not file_create(year_configs_folder, "data.csv", DEFAULT_DATA)
    ):
        return False
    if not file_create(year_configs_folder, "configs.csv", DEFAULT_YEAR_CONFIGS):
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
        not directory_create(month_folder) or 
        not directory_create(month_data_folder) or 
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
print(read_csv("./test.csv"))