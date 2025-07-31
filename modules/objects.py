from os import path
from modules.inputs import read_csv, helper, find_row, find_data_files, find_summed, find_targets

class SubGoal:
    def __init__(self, 
                 path_to_graph: str, 
                 sub_goal: str, 
                 target_num: float, 
                 num: float, 
                 num_color: str, 
                 time: str, 
                 committee: str, 
                 show_graph: bool):
        self.path_to_graph: str = path_to_graph
        self.sub_goal: str = sub_goal
        self.target_num: float = target_num
        self.num: float = num
        self.num_color: str = num_color
        self.time: str = time
        self.committee: str = committee
        self.show_graph: bool = show_graph
        
    def __eq__(self, value: object) -> bool:
        if type(value) is not SubGoal or value.sub_goal != self.sub_goal:
            return False
        return True
    
class SubGoals:
    def __init__(self, sub_goal_content: list[str], path_to_report: str, month: int, affix: str):
        
        self.sub_goal: str = sub_goal_content[0]
        self.time: str = sub_goal_content[2]
        self.committee: str = sub_goal_content[4]
        self.show_graph: bool = (sub_goal_content[5] == "True")
        self.current_sum: float = self.find_current_sum(sub_goal_content[3], sub_goal_content[1], path_to_report, month)
        target: tuple[float, float] = self.find_targets(path_to_report, month)
        self.target: float = target[1]
        self.color: str = "#000000"
        if target[0] != 0:
            ratio = self.current_sum / target[0]
            if ratio > 1.2:
                self.color = "#0000FF"
            elif ratio > .8:
                self.color = "#009900"
            elif ratio > .6:
                self.color = "#FF9900"
            else:
                self.color = "#BB0000"
        self.path_to_graph: str = ""
        if self.show_graph:
            self.path_to_graph = path.join(path_to_report, "outputs", "graphs", f"{self.sub_goal}{affix}_graph.png")
        
    def __eq__(self, value: object) -> bool:
        if type(value) is not SubGoals or value.sub_goal != self.sub_goal:
            return False
        return True
    
    def find_current_sum(self, summed_column: str, data_file: str, path_to_report: str, month: int) -> float:
        path_to_data: str = path.join(path_to_report, "inputs", "data")
        data_files: list[list[list[str]]] = find_data_files(data_file, path_to_data)
        return find_summed(self.time, summed_column, data_files, month)
        
    def find_targets(self,path_to_report: str, month: int) -> tuple[float, float]:
        path_to_target: str = path.join(path_to_report, "inputs", "targets")
        target_file: list[list[str]] = read_csv(path_to_target, f"{self.sub_goal}_targets.csv")
        return find_targets(self.time, target_file, month)
    
class Goal:
    def __init__(self, goal_content: list[str], path_to_report: str, month: int, affix: str):
        
        self.goal: str = goal_content[0]
        try:
            self.percentage: float = float(goal_content[1])
        except ValueError:
            print(f"\033[0;31mError: The goal `{self.goal}` has a non-number percentage `{goal_content[1]}`. Setting value to 50.\033[0m")
            log(f"\033[0;31mError: The goal `{self.goal}` has a non-number percentage `{goal_content[1]}`. Setting value to 50.\033[0m")
            self.percentage: float = 50.0
        except Exception as e:
            print(f"\033[0;31mError: The goal `{self.goal}` has an improper percentage `{goal_content[1]}` resulting in {e}. Setting value to 50.\033[0m")
            log(f"\033[0;31mError: The goal `{self.goal}` has an improper percentage `{goal_content[1]}` resulting in {e}. Setting value to 50.\033[0m")
            self.percentage: float = 50.0
        self.sub_goals: list[SubGoals] = self.generate_sub_goals(helper(goal_content[2]), path_to_report, month, affix)
        self.extra_text: list[str] = self.find_extra_text(path_to_report, affix)
    
    def generate_sub_goals(self, sub_goals_names: list[str], path_to_report: str, month: int, affix: str) -> list[SubGoals]:

        sub_goals: list[SubGoals] = []
        
        path_to_sub_goals: str = path.join(path_to_report, "configs")
        data: list[list[str]] = read_csv(path_to_sub_goals, "sub_goals.csv")
        
        for sub_goal in sub_goals_names:
            row: int = find_row(data, sub_goal)
            sub_goals.append(SubGoals(data[row], path_to_report, month, affix))

        return sub_goals
    
    def find_extra_text(self, path_to_report: str, affix: str) -> list[str]:
        
        extra_text: list[str] = []
        path_to_goal_extras: str = path.join(path_to_report, "configs")
        try:
            with open(path.join(path_to_goal_extras, f"{self.goal}_extras{affix}.txt"), 'r') as file:
                for line in file:
                    extra_text.append(line)
        except Exception as e:
            print(f"\033[0;31mError: {e}.\033[0m")
            log(f"\033[0;31mError: {e}.\033[0m")
        return extra_text
    
def log(log: str):
    pass
    # configs = get_app_configs(resource_path(), "configs.csv")
    # home_dir = resource_path(configs[find_row(configs, "home_directory")][1])
    # logs = path.join(home_dir, "logs")
    
    # with open(path.join(logs, "logs.txt"), 'a') as file:
    #     file.write(f"{log}\n")

# def create_log():