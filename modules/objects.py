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
    