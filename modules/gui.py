from __future__ import annotations
import customtkinter as ctk
from typing import Any, Callable
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from PIL import Image
from modules.inputs import write_csv, read_csv, delete_csv, helper, find_row, find_data_files, find_summed, find_targets, find_graph_data, find_or_create_data_files, find_or_create_target_files, find_column, create_csv
from modules.objects import SubGoal, Goal
from modules.directory_management import report_generation, report_finalization, new_report_version, has_report_pdf_generated
from os import path
# comp_year_color = "#CC0000"
# target_color = "#008800"
# year_color = "#0000CC"



class Page(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
    def show(self):
        self.lift()

class CSVRow(ctk.CTkFrame):
    def __init__(self, master, data: list[str] = [], length: int = 0):
        super().__init__(master)
        
        self.grid_rowconfigure(0, weight=0)
    
        self.cells: list[ctk.CTkTextbox] = []
        
        for cell in data:
            self.grid_columnconfigure(len(self.cells), weight=1)
            textbox = ctk.CTkTextbox(self, height=80)
            textbox.insert("0.0", cell)
            textbox.grid(row=0, column=len(self.cells), sticky="nsew")
            self.cells.append(textbox)
            
        if not data:
            for i in range(length):
                self.grid_columnconfigure(len(self.cells), weight=1)
                textbox = ctk.CTkTextbox(self, height=80)
                textbox.insert("0.0", "")
                textbox.grid(row=0, column=len(self.cells), sticky="nsew")
                self.cells.append(textbox)
            
    def has_row_changed(self, data) -> bool:
        for i in range(len(self.cells)):
            content = self.cells[i].get("0.0", "end-1c")
            if content != data[i]:
                return True
        return False
    
    def get_row(self) -> list[str]:
        data: list[str] = []
        for i in range(len(self.cells)):
            content = self.cells[i].get("0.0", "end-1c")
            data.append(content)
        return data
        
class ScrollableCSVFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.rows: list[tuple[ctk.CTkFrame, CSVRow]] = []
        self.length = 0
        
        self.add_row_button: ctk.CTkButton = ctk.CTkButton(self, text="Add Row", command=self.add_row)
        self.update_row_button()
    
    def update_row_button(self):
        self.add_row_button.grid(row=len(self.rows), column=0, sticky="nsew")
    
    def add_rows(self, data: list[list[str]]):
        self.length = len(data[0])
        self.destroy_rows()
        for row in data[1:]:
            self.add_row(row)
            
        self.update_row_button()
        
    def add_row(self, row_data: list[str] = []):
        row_frame = ctk.CTkFrame(self)
        row_frame.grid(row=len(self.rows), column=0, sticky="ew")
        row_frame.grid_columnconfigure(0, weight=0)
        row_frame.grid_columnconfigure(0, weight=0)
        row_frame.grid_columnconfigure(1, weight=1)
        row_frame.grid_columnconfigure(3, weight=0)
        
        arrow_frame = ctk.CTkFrame(row_frame)
        arrow_frame.grid(row=0, column=0, sticky="nsew")
        arrow_frame.grid_rowconfigure(0, weight=0)
        arrow_frame.grid_rowconfigure(1, weight=0)
        arrow_frame.grid_columnconfigure(0, weight=1)
        
        new_row = CSVRow(row_frame, row_data, length=self.length)
        new_row.grid(row=0, column=1, sticky="ew")

        up_button = ctk.CTkButton(arrow_frame, text="^", width=40, command=lambda: self.move_row((row_frame, new_row), -1))
        up_button.grid(row=0, column=0, sticky="new")
        
        down_button = ctk.CTkButton(arrow_frame, text="v", width=40, command=lambda: self.move_row((row_frame, new_row), 1))
        down_button.grid(row=1, column=0, sticky="sew")
        
        delete_button = ctk.CTkButton(row_frame, text="Delete", width=40, fg_color="red", command=lambda: self.delete_row((row_frame, new_row)))
        delete_button.grid(row=0, column=2, sticky="ew")
        
        self.rows.append((row_frame, new_row))
        if not row_data:
            self.update_row_button()
    
    def move_row(self, row: tuple[ctk.CTkFrame, CSVRow], move_by: int):
        index = self.rows.index(row)
        index += move_by
        if index < 0 or index >= len(self.rows):
            return
        self.rows.remove(row)
        self.rows.insert(index, row)    
        self.update_rows_position()
    
    def delete_row(self, row: tuple[ctk.CTkFrame, CSVRow]):
        row[0].grid_remove()
        self.rows.remove(row)
        self.update_rows_position()
    
    def update_rows_position(self):
        for i in range(len(self.rows)):
            self.rows[i][0].grid(row=i, column=0, sticky="nsew")
        self.update_row_button()
    
    def populate_rows(self, data: list[list[str]]): # Delete This.
        self.add_rows(data)
    
    def destroy_rows(self):
        while len(self.rows) > 0:
            row = self.rows.pop(0)
            row[0].destroy()
        self.update_row_button()
    
    def has_changed(self, data: list[list[str]]) -> bool:
        if len(data) != len(self.rows):
            return True
        for i in range(len(self.rows)):
            if self.rows[i][1].has_row_changed(data[i]):
                return True
        return False
    
    def get_data(self) -> list[list[str]]:
        data: list[list[str]] = []
        for row in self.rows:
            data.append(row[1].get_row())
        return data

class CSVFrame(Page):
    def __init__(self, master, save_csv):
        super().__init__(master)
        
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.data: list[list[str]] = [[""]]
        self.save_csv = save_csv
        
        self.quit_without_saving = False
        
        self.data_source_label = ctk.CTkLabel(self, text="")
        self.data_source_label.grid(row=0, column=0, stick="new")
        
        self.data_frame = ctk.CTkFrame(self)
        self.data_frame.grid(row=1, column=0, sticky="nsew")
        self.data_frame.grid_rowconfigure(0, weight=0)
        self.data_frame.grid_rowconfigure(1, weight=1)
        self.data_frame.grid_rowconfigure(2, weight=0)
        self.data_frame.grid_columnconfigure(0, weight=1)
        
        
        self.data_columns_frame = ctk.CTkFrame(self.data_frame)
        self.data_columns_frame.grid(row=0, column=0, sticky="nsew")
        self.data_columns_frame.grid_rowconfigure(0, weight=0)
        self.data_columns = []
        
        self.data_entires = ScrollableCSVFrame(self.data_frame)
        self.data_entires.grid(row=1, column=0, sticky="nsew")
        
        self.save_buttons_frame = ctk.CTkFrame(self)
        self.save_buttons_frame.grid(row=2, column=0, sticky="nsew")
        self.save_buttons_frame.grid_rowconfigure(0, weight=0)
        self.save_buttons_frame.grid_columnconfigure(0, weight=1)
        
        self.save_button = ctk.CTkButton(self.save_buttons_frame, text="save", command=save_csv)
        self.save_button.grid(row=0, column=0, sticky="nsew")
        

    def save_changes(self) -> list[list[str]]:
        output_data: list[list[str]] = []
        
        if self.data_entires.has_changed(self.data[1:]):
            data_columns = []
            for column in self.data_columns:
                data_columns.append(column.cget("text"))
            output_data = self.data_entires.get_data()
            output_data.insert(0, data_columns)
            self.data = output_data
            return output_data
        
        return []
    
    def has_changed(self) -> bool:
        return self.data_entires.has_changed(self.data[1:])
    
    def close(self):
        self.data_entires.destroy_rows()
        
    def populate_CSV_frame(self, name_of_file, data):
        self.close()
        self.data = data
        self.data_source_label.configure(text=name_of_file)
        self.populate_column(data[0])
        self.data_entires.populate_rows(data)
        
    def populate_column(self, columns):
        while len(self.data_columns) > 0:
            label = self.data_columns.pop(0)
            label.destroy()
        number = 0
        for column in columns:
            self.data_columns_frame.grid_columnconfigure(number, weight=1)
            label = ctk.CTkLabel(self.data_columns_frame, text=column)
            label.grid(row=0, column=number, sticky="nsew")
            self.data_columns.append(label)
            number += 1

class SubGoalFrame(Page):
    def __init__(self, master, data_button: Callable, left: Callable, right: Callable):
        super().__init__(master)
        
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.show_graph_checkbox = ctk.CTkCheckBox(self, text="Show Graph", command=self.show_graph)
        self.show_graph_checkbox.grid(row=0, column=0, sticky="e")
        
        self.body_frame = ctk.CTkFrame(self)
        self.body_frame.grid(row=1, column=0, sticky="nsew")
        self.body_frame.grid_rowconfigure(0, weight=1)
        self.body_frame.grid_columnconfigure(0, weight=0)
        self.body_frame.grid_columnconfigure(1, weight=1)
        self.body_frame.grid_columnconfigure(2, weight=0)
        
        self.left_arrow = ctk.CTkButton(self.body_frame, text="<", command=left, width=40)
        self.left_arrow.grid(row=0, column=0, sticky="nsew")
        
        self.right_arrow = ctk.CTkButton(self.body_frame, text=">", command=right, width=40)
        self.right_arrow.grid(row=0, column=2, sticky="nsew")
        
        
        self.content_frame = ctk.CTkFrame(self.body_frame)
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.grid_rowconfigure(0, weight=0)
        self.content_frame.grid_rowconfigure(1, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # self.sub_goal_container_frame = ctk.CTkFrame(self.content_frame)
        # # self.sub_goal_container_frame.configure(fg_color="#FF0000")
        # self.sub_goal_container_frame.grid(row=0, column=0, sticky="nsew")

        self.sub_goal_data_frame = ctk.CTkFrame(self.content_frame)
        self.sub_goal_data_frame.grid(row=0, column=0, sticky="nsew")
        # self.sub_goal_data_frame.grid_propagate(False)
        self.sub_goal_data_frame.grid_rowconfigure(0, weight=0)
        self.sub_goal_data_frame.grid_rowconfigure(1, weight=0)
        self.sub_goal_data_frame.grid_rowconfigure(2, weight=0)
        self.sub_goal_data_frame.grid_rowconfigure(3, weight=0)
        self.sub_goal_data_frame.grid_columnconfigure(0, weight=1)
        self.sub_goal_data_frame.bind("<Button-1>", command=data_button)
        self.sub_goal_data_frame.configure(cursor="hand2")

        self.sub_goal_label = ctk.CTkLabel(self.sub_goal_data_frame, text="s")
        self.sub_goal_label.grid(row=0, column=0, sticky="nsew")
        self.sub_goal_label.bind("<Button-1>", command=data_button)

        self.sub_goal_sum_label = ctk.CTkLabel(self.sub_goal_data_frame, text="f")
        self.sub_goal_sum_label.grid(row=1, column=0, sticky="nsew")
        self.sub_goal_sum_label.bind("<Button-1>", command=data_button)
        
        self.sub_goal_target_label = ctk.CTkLabel(self.sub_goal_data_frame, text="d")
        self.sub_goal_target_label.grid(row=2, column=0, sticky="nsew")
        self.sub_goal_target_label.bind("<Button-1>", command=data_button)
        
        self.sub_goal_committee_label = ctk.CTkLabel(self.sub_goal_data_frame, text="w")
        self.sub_goal_committee_label.grid(row=3, column=0, sticky="nsew")
        self.sub_goal_committee_label.bind("<Button-1>", command=data_button)
        
        # self.sub_goal_csv_button = ctk.CTkButton(
        #     self.sub_goal_container_frame, 
        #     text=" ",
        #     fg_color="transparent",
        #     hover=False,
        #     command=lambda: print("hello"))
        # self.sub_goal_csv_button.place(x=0, y=0, relwidth=1, relheight=1)
        # self.sub_goal_csv_button.lower()
        
        
        self.graph_frame = ctk.CTkFrame(self.content_frame)
        # self.graph_frame.configure(fg_color="#FFFFFF")
        self.graph_frame.grid(row=1, column=0, sticky="nsew")
        self.graph_frame.grid_rowconfigure(0, weight=1)
        self.graph_frame.grid_columnconfigure(0, weight=1)
        
        self.graph_path = ""
        
        self.graph_label = ctk.CTkLabel(self.graph_frame, text=" ")
        self.graph_label.grid(row=0, column=0, sticky="nsew")
        
        self.show_graph()
    
    def show_graph(self):
        if self.show_graph_checkbox.get():
            self.content_frame.grid_rowconfigure(0, weight=0)
            self.content_frame.grid_rowconfigure(1, weight=1)
            self.graph_frame.grid()
        else:
            self.content_frame.grid_rowconfigure(0, weight=1)
            self.content_frame.grid_rowconfigure(1, weight=0)
            self.graph_frame.grid_remove()

    def set_graph(self, graph_path):
        self.graph_path = graph_path
        graph = Image.open(self.graph_path)
        graph_image = ctk.CTkImage(light_image=graph, size=(400, 300))
        self.graph_label.configure(image=graph_image)
    
    def populate_sub_goal_data(self, sub_goal: str, sum: float, target_num: float, target_text: str, committee: str, show_graph: bool):
        self.sub_goal_label.configure(text=sub_goal)
        self.sub_goal_sum_label.configure(text=str(sum))
        #TODO: Calculate sum color.
        self.sub_goal_target_label.configure(text=target_text)
        self.sub_goal_committee_label.configure(text=committee)
        if show_graph:
            self.show_graph_checkbox.select()
        else:
            self.show_graph_checkbox.deselect()
        self.show_graph()

class GoalFrame(Page):
    def __init__(self, master, left: Callable, generate_pdf: Callable, save: Callable):
        super().__init__(master)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        
        self.left_arrow = ctk.CTkButton(self, text="<", command=left, width=40)
        self.left_arrow.grid(row=0, column=0, sticky="nsew")
        
        self.generate_pdf_button = ctk.CTkButton(self, text="Generate PDF", command=generate_pdf, width=40)
        self.generate_pdf_button.grid(row=0, column=2, sticky="nsew")
        
        self.body_frame = ctk.CTkFrame(self)
        self.body_frame.grid(row=0, column=1, sticky="nsew")
        self.body_frame.grid_rowconfigure(0, weight=1)
        self.body_frame.grid_rowconfigure(1, weight=0)
        self.body_frame.grid_columnconfigure(0, weight=1)
        
        self.goal_frame = ScrollableGoalFrame(self.body_frame)
        self.goal_frame.grid(row=0, column=0, sticky="nsew")
        
        self.save_button = ctk.CTkButton(self.body_frame, text="Save Data", command=save)
        self.save_button.grid(row=1, column=0, sticky="ew")
        
    def populate_goals(self, goals: list[list[str]], path_to_report: str, affix: str):
        self.goal_frame.add_goals(goals[1:], path_to_report, affix)
        
    def save_data(self) -> list[tuple[str, str]]:
        return self.goal_frame.out_load_data()
    
    def has_changed(self) -> bool:
        for goal in self.goal_frame.goals:
            if goal.has_changed():
                return True
        return False
        

class HelperGoalFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.goal_number = ctk.CTkLabel(self, text=f"GOAL 0")
        self.goal_number.grid(row=0, column=0, sticky="ew")
        
        self.goal_name = ctk.CTkLabel(self, text="")
        self.goal_name.grid(row=1, column=0, sticky="ew")
        
        self.goal_percent_num = ""
        self.goal_percent = ctk.CTkTextbox(self, height=80)
        # goal_percent.insert("0.0", goal[1])
        self.goal_percent.grid(row=2, column=0, sticky="ew")
        
        self.extra_data = ""
        self.goal_extra_data = ctk.CTkTextbox(self, height=80)
        # goal_extra_data.insert("0.0", goal[3])
        self.goal_extra_data.grid(row=3, column=0, sticky="ew")
        
    def update_percent(self):
        self.goal_percent_num = self.get_percent()
    
    def update_extra_data(self):
        self.extra_data = self.get_extra_data()
    
    def get_percent(self) -> str:
        try:
            return str(float(self.goal_percent.get("0.0", "end-1c").strip()))
        except:
            print("ERROR")
            log("ERROR")
            return "0.0"
    
    def set_extra_data(self, path_to_report: str, affix: str):
        
        extra_text: str = ""
        path_to_goal_extras: str = path.join(path_to_report, "configs")
        try:
            with open(path.join(path_to_goal_extras, f"{self.goal_name.cget("text")}_extras{affix}.txt"), 'r') as file:
                extra_text = file.read()
        except FileNotFoundError:
            print(f"\033[0;31mError: The file `{self.goal_name.cget("text")}_extras{affix}.txt` doesn't exist. Creating it.\033[0m")
            log(f"\033[0;31mError: The file `{self.goal_name.cget("text")}_extras{affix}.txt` doesn't exist. Creating it.\033[0m")
            create_csv(path_to_goal_extras, f"{self.goal_name.cget("text")}_extras{affix}.txt", [])
        self.extra_data = extra_text
        self.goal_extra_data.insert("0.0", extra_text)
    
    def get_extra_data(self) -> str:
        return self.goal_extra_data.get("0.0", "end-1c").strip()
    
    def has_changed(self) -> bool:
        return self.extra_data != self.get_extra_data() or self.goal_percent_num != self.get_percent()

class ScrollableGoalFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, orientation="horizontal")
        
        
        self.grid_rowconfigure(0, weight=1)
        self.goals: list[HelperGoalFrame] = []
        
    def add_goals(self, goals: list[list[str]], path_to_report: str, affix: str):
        
        self.goals.clear()
        for goal in goals:
            self.add_goal(goal, path_to_report, affix)
    
    def add_goal(self, goal: list[str], path_to_report: str, affix: str):
        
        g = HelperGoalFrame(self)
        self.grid_columnconfigure(len(self.goals), weight=1)
        g.grid(row=0, column=len(self.goals), sticky="nsew")
        
        g.goal_number.configure(text=f"GOAL {len(self.goals) + 1}")
        g.goal_name.configure(text=goal[0])
        g.goal_percent.insert("0.0", goal[1])
        g.set_extra_data(path_to_report, affix)
        # g.goal_extra_data.insert("0.0", goal[3])
        
        self.goals.append(g)
    
    def out_load_data(self) -> list[tuple[str, str]]:
        output: list[tuple[str, str]] = []
        for goal in self.goals:
            output.append((goal.get_percent(), goal.get_extra_data()))
            goal.update_percent()
            goal.update_extra_data()
        return output

class ScrollableButtonFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, open_object):
        super().__init__(master)
        
        self.grid_columnconfigure(0, weight=1)
        self.open_object = open_object
        self.buttons = []
        
    def add_buttons(self, buttons: list[tuple[str, str]]):
        for button_path, name in buttons:
            self.add_button(button_path, name)
        
    def add_button(self, button_path: str, name: str):
        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=len(self.buttons), column=0, padx=10, pady=10, sticky="ew") # When a button is deleted, the rows get out of line. This has no visual effect.
        button_frame.grid_rowconfigure(0, weight=1)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=0)
        self.buttons.append(button_frame)
        
        new_button = ctk.CTkButton(button_frame, text=name, command=lambda: self.open_object(button_path, name))
        new_button.grid(row=0, column=0, sticky="ew")
        
        delete_button = ctk.CTkButton(button_frame, fg_color="red", text="Delete", width=40, command=lambda: self.delete_button(button_path, button_frame))
        delete_button.grid(row=0, column=1, sticky="e")
        
    
    def delete_button(self, button_path: str, button_frame: ctk.CTkFrame):
        self.buttons.remove(button_frame)
        button_frame.destroy()
        delete_csv(button_path)
    
    def delete_buttons(self):
        while len(self.buttons) > 0:
            button = self.buttons.pop(0)
            button.destroy()
   
class ReportValidationPage(Page):
    def __init__(self, master, create_graph):
        super().__init__(master)
        
        
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        # self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)
        
        self.goal_heading = ctk.CTkLabel(self, text="Goal Heading")
        self.goal_heading.grid(row=0, column=0, sticky="ew")
        
        self.sub_goal_frame = ctk.CTkFrame(self)
        self.sub_goal_frame.grid(row=1, column=0, sticky="nsew")
        
        self.sub_goal_data = CSVFrame(self.sub_goal_frame, self.save_csv)
        self.sub_goal_data.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.sub_goal = SubGoalFrame(self.sub_goal_frame, self.open_data, self.left_arrow, self.right_arrow)
        self.sub_goal.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.goal_data = GoalFrame(self.sub_goal_frame, self.left_arrow, self.generate_pdf, self.save_goals)
        self.goal_data.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.sub_goal.show()
        
        # self.save_report_button = ctk.CTkButton(self, text="Save Report", command=lambda: print("Save Report"))
        # self.save_report_button.grid(row=2, column=0, sticky="sew")
        
        self.data_active = False
        
        self.create_graph = create_graph
        
        self.goals = []
        self.goals_sub_goals = []
        self.sub_goals = []
        self.current_goal = -1
        self.current_sub_goal = -1
        self.current_sub_goal_data = []
        
        self.allow_edit = True
        
        self.access_directory = ""
        self.affix = ""
        
        self.path_to_year = ""
        self.path_to_report = ""
        self.report_name = ""
        self.year = ""
        self.path_to_comp_data = ""
        self.month = 0
        self.current_year = 0
        self.comp_year = 0
        self.override_quit = False
    
    def save_goals(self):
        
        data = self.goal_data.save_data()
        
        for i in range(1, len(self.goals)):
            self.goals[i][1] = data[i - 1][0]
            # self.goals[i][3] = data[i - 1][1]
            with open(path.join(self.path_to_report, "configs", f"{self.goals[i][0]}_extras{self.affix}.txt"), 'w') as file:
                file.write(data[i - 1][1])
        
        write_csv(path.join(self.access_directory, "configs"), "goals.csv", self.goals) #TODO: The percentage shouldn't be stored in the year folder...
    
    def save_csv(self):
        
        data = self.sub_goal_data.save_changes()
        if not data:
            return
        row = find_row(self.sub_goals, self.goals_sub_goals[self.current_goal][self.current_sub_goal])
        if row == -1:
            return
        sub_goal: list[str] = self.sub_goals[row]
        self.current_sub_goal_data = []
        write_csv(path.join(self.access_directory, "inputs", "data"), f"{sub_goal[1]}{self.affix}.csv", data)
        
    
    def has_changed(self):
        return self.sub_goal_data.has_changed()
    
    def open_data(self, event):
        if not self.allow_edit:
            return
        row = find_row(self.sub_goals, self.goals_sub_goals[self.current_goal][self.current_sub_goal])
        if row == -1:
            return
        sub_goal: list[str] = self.sub_goals[row]
        self.current_sub_goal_data = read_csv(path.join(self.access_directory, "inputs", "data"), f"{sub_goal[1]}{self.affix}.csv")
        self.sub_goal_data.populate_CSV_frame(f"{sub_goal[1]}{self.affix}.csv", self.current_sub_goal_data)
        self.data_active = True
        self.sub_goal_data.show()
    
    def close_data(self):
        self.current_sub_goal_data = []
        self.override_quit = False
        self.sub_goal_data.close()
        self.data_active = False
        self.generate_sub_goal()
        self.sub_goal.show()
        
    def create_report(self, 
                      path_to_report: str,
                      version: str,
                      path_to_year: str, 
                      year: str,  
                      month: int, 
                      current_year: int = 0, 
                      comp_year: int = 0, 
                      path_to_comp_year: str = ""):
        
        
        configs_path = path.join(path_to_report, "configs")
        configs = read_csv(configs_path, "configs.csv")
        
        
        self.access_directory = configs[find_row(configs, "access_directory")][1]
        self.affix = ""
        if version != "1":
            self.affix = f"_{version}"
        
        self.allow_edit = not has_report_pdf_generated(path_to_report, self.affix)
        
        self.goals = read_csv(path.join(self.access_directory, "configs"), "goals.csv")
        self.sub_goals = read_csv(path.join(self.access_directory, "configs"), "sub_goals.csv")
        self.goals_sub_goals = []
        for row in range(len(self.goals)):
            # print(self.goals[row][2])
            self.goals_sub_goals.append(helper(self.goals[row][2]))

        self.goal_heading.configure(text=self.goals[1][0])
        self.current_goal = 1
        self.current_sub_goal = 0
        # self.sub_goal_objects: list[tuple[list[Any], list[SubGoal]]] = []
        # for goal in self.goals:
            # self.sub_goal_objects.append((goal, []))
        
        self.report_name = f"{configs[find_row(configs, 'month')][1]} Report"
        self.path_to_year = path_to_year
        self.year = year
        self.path_to_report = path_to_report
        self.month = month
        self.current_year = current_year
        self.comp_year = comp_year
        self.path_to_comp_year = path_to_comp_year
        
    def editing(self):
        
        pass
    
    def left_arrow(self):
        self.current_sub_goal -= 1
        if self.current_sub_goal < 0:
            self.current_goal -= 1
            self.current_sub_goal = len(self.goals_sub_goals[self.current_goal]) - 1
            self.goal_heading.configure(text=self.goals[self.current_goal][0])
        self.generate_sub_goal()
    
    def right_arrow(self):
        self.current_sub_goal += 1

        if self.current_sub_goal == len(self.goals_sub_goals[self.current_goal]):
            self.current_goal += 1
            self.current_sub_goal = 0
            if self.current_goal == len(self.goals):
                self.goal_data.populate_goals(self.goals, self.path_to_report, self.affix)
                self.goal_data.show()
                return
            self.goal_heading.configure(text=self.goals[self.current_goal][0])
        else:
            self.sub_goal.right_arrow.configure(text=">")
            self.sub_goal.right_arrow.configure(state="normal")
        self.generate_sub_goal()
    
    def generate_pdf(self, quit_without_saving = False):
        
        if not quit_without_saving and self.goal_data.has_changed():
            save_or_quit_goal(self.goal_data, self.save_goals, self.generate_pdf)
            return
        
        report_finalization(self.path_to_report)
        
        goal_obj: list[Goal] = []
        for goal in self.goals[1:]:
            goal_obj.append(Goal(goal, self.path_to_report, self.month, self.affix)) # This is less efficient but neater.
        
        report_generation(self.path_to_report, self.report_name, self.year, goal_obj, self.affix)
    
    def generate_sub_goal(self): #! This is inefficient. Why regenerate the sub_goal if it hasn't changed? If we're just switching panels, it doesn't matter.
        row = find_row(self.sub_goals, self.goals_sub_goals[self.current_goal][self.current_sub_goal])
        if row == -1:
            return
        sub_goal: list[str] = self.sub_goals[row]
        data_files = find_data_files(sub_goal[1], path.join(self.access_directory, "inputs", "data"), self.affix)
        # print(data_files)
        current_sum: float = find_summed(sub_goal[2], sub_goal[3], data_files, self.month)

        self.editing()

        comp_data_files = []
        # print(self.path_to_comp_year)
        if self.path_to_comp_year:
            comp_data_files = find_data_files(sub_goal[1], path.join(self.path_to_comp_year, "inputs", "data"))
            # print(comp_data_files)
            # comp_current_sum: float = find_summed(sub_goal[2], sub_goal[3], comp_data_files, month)
        target_file = read_csv(path.join(self.access_directory, "inputs", "targets"), f"{sub_goal[0]}_targets.csv")
        targets: tuple[float, float] = find_targets(sub_goal[2], target_file, self.month)
        
        # print(data_files)
        
        graph_data = find_graph_data(sub_goal[2], 
                                     sub_goal[3], 
                                     data_files, 
                                     target_file, 
                                     comp_data_files, self.month)
        self.sub_goal.set_graph(self.create_graph(
                                sub_goal[0], 
                                sub_goal[3], 
                                self.current_year, 
                                graph_data[0], 
                                graph_data[1], 
                                self.path_to_report, 
                                graph_data[2], 
                                self.comp_year,
                                self.affix))
        
        if sub_goal[5] == "True":
            set_graph: bool = True
        else:
            set_graph: bool = False
            
        if targets[0] != 0:
            ratio = current_sum / targets[0]
            if ratio > 1.2:
                num_color = "#0000FF"
            elif ratio > .8:
                num_color = "#009900"
            elif ratio > .6:
                num_color = "#FF9900"
            else:
                num_color = "#BB0000"
            
            self.goals[self.current_goal][1] = float(self.goals[self.current_goal][1]) * (ratio + 0.2)
            # self.sub_goal_objects[self.current_goal][0][1] = self.sub_goal_objects[self.current_goal][0][1] * (ratio + 0.2)
            # if self.sub_goal_objects[self.current_goal][0][1] > 100:
                # self.sub_goal_objects[self.current_goal][0][1] = 100
        else:
            num_color = "#000000"
        # print(set_graph)
        # sg = SubGoal(resource_uri(path.join(self.path_to_report, "outputs", "graphs", f"{sub_goal[0]}.png")), sub_goal[0], targets[1], current_sum, num_color, sub_goal[2], sub_goal[4], set_graph)
        self.sub_goal.populate_sub_goal_data(sub_goal[0], current_sum, targets[0], f"{sub_goal[2]} Goal: {targets[1]}", f"{sub_goal[4]} Committee", set_graph)

        # index = len(self.sub_goal_objects[self.current_goal][1])
        # if sg in self.sub_goal_objects[self.current_goal][1]:
            # index = self.sub_goal_objects[self.current_goal][1].index(sg)
            # self.sub_goal_objects[self.current_goal][1].pop(index)
        # self.sub_goal_objects[self.current_goal][1].insert(index, sg)
        if self.current_sub_goal == 0 and self.current_goal == 1:
            self.sub_goal.left_arrow.configure(state="disabled")
        else:
            self.sub_goal.left_arrow.configure(state="normal")
        self.sub_goal.show()

class ReportSelection(Page):
    def __init__(self, master: App, open_report_version: Callable):
        super().__init__(master)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)
        
        self.report_name = ctk.CTkLabel(self, text="s")
        self.grid(row=0, column=0, sticky="new")
        
        self.report_versions = ctk.CTkOptionMenu(self, values=[])
        self.report_versions.grid(row=1, column=0, sticky="ew")
        
        self.path_to_report = ""
        self.month = ""
        
        self.proceed = ctk.CTkButton(self, text="Proceed", command=lambda: open_report_version(self.path_to_report, self.report_versions.get(), self.month))
        self.proceed.grid(row=2, column=0, sticky="sew")
    
    def report_selection(self, path_to_report: str, versions: list[str], month: str):
        self.report_name.configure(text="month")
        self.path_to_report = path_to_report
        self.month = month
        versions.append("Create New")
        self.report_versions.configure(values=versions)
        self.report_versions.set(versions[0])

class NewReportPage(Page):
    def __init__(self, master: App, create_report: Callable):
        super().__init__(master)
        
        self.grid_propagate(False)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        # self.grid_rowconfigure(3, weight=0)
        self.grid_columnconfigure(0, weight=1)
        
        self.year = ctk.CTkLabel(self, text="")
        self.year.grid(row=0, column=0, sticky="ew")
        
        self.path_to_year = ""
        
        values = ["Jul", "Aug", "Sep", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        self.months = ctk.CTkOptionMenu(self, values=values, command=self.check_if_duplicate)
        self.months.grid(row=1, column=0, sticky="ew")
        
        self.already_taken = ctk.CTkLabel(self, text="")
        # self.already_taken.grid(row=2, column=0, sticky="ew")
        
        self.create_button = ctk.CTkButton(self, text="Create", command= lambda: create_report(self.path_to_year, self.months.get()))
        self.create_button.grid(row=2, column=0, sticky="ew")
    
    def check_if_duplicate(self, month):
        # if month in self.master.reports:
        #TODO: Implement.
        pass
        
    def initialize(self, year: str, path_to_year: str, month: str):
        self.year.configure(text=year)
        self.path_to_year = path_to_year
        self.months.set(month)
        
class EditYearPage(Page):
    def __init__(self, master: App):
        super().__init__(master)
        
        self.edit_homepage = Page(self)
        self.edit_homepage.place(in_=self, x=0, y=0, relwidth=1, relheight=1)
        self.edit_homepage.grid_rowconfigure(0, weight=1)
        self.edit_homepage.grid_rowconfigure(1, weight=1)
        self.edit_homepage.grid_rowconfigure(2, weight=1)
        self.edit_homepage.grid_rowconfigure(3, weight=1)
        self.edit_homepage.grid_rowconfigure(4, weight=1)
        self.edit_homepage.grid_rowconfigure(5, weight=1)
        self.edit_homepage.grid_columnconfigure(0, weight=1)
        
        self.current_page = ""
        self.path_to_year = ""
        self.path_to_file = ""
        self.name_of_file = ""
        
        self.edit_data = ctk.CTkButton(self.edit_homepage, text="Edit Data", command=self.open_data)
        self.edit_data.grid(row=0, column=0, sticky="nsew")
        
        self.edit_data = ctk.CTkButton(self.edit_homepage, text="Edit Data Content", command=self.open_data_content)
        self.edit_data.grid(row=1, column=0, sticky="nsew")
        
        self.edit_data = ctk.CTkButton(self.edit_homepage, text="Edit Targets", command=self.open_targets)
        self.edit_data.grid(row=2, column=0, sticky="nsew")
        
        self.edit_data = ctk.CTkButton(self.edit_homepage, text="Edit Configs", command=self.open_configs)
        self.edit_data.grid(row=3, column=0, sticky="nsew")
        
        self.edit_data = ctk.CTkButton(self.edit_homepage, text="Edit Goals", command=self.open_goals)
        self.edit_data.grid(row=4, column=0, sticky="nsew")
        
        self.edit_data = ctk.CTkButton(self.edit_homepage, text="Edit Sub-Goals", command=self.open_sub_goals)
        self.edit_data.grid(row=5, column=0, sticky="nsew")
        
        self.edit_menu_page = Page(self)
        self.edit_menu_page.place(in_=self, x=0, y=0, relwidth=1, relheight=1)
        self.edit_menu_page.grid_rowconfigure(0, weight=1)
        self.edit_menu_page.grid_columnconfigure(0, weight=1)

        
        self.edit_menu = ScrollableButtonFrame(self.edit_menu_page, self.open_file)
        self.edit_menu.grid(row=0, column=0, sticky="nsew")
        
        self.edit_csv_page = CSVFrame(self, self.save_csv)
        self.edit_csv_page.place(in_=self, x=0, y=0, relwidth=1, relheight=1)
        
        
        
    def initialize(self, path_to_year):
        self.path_to_year = path_to_year
        self.open_homepage()
        pass
        
    def save_csv(self):
        data = self.edit_csv_page.save_changes()
        if not data:
            return
        write_csv(self.path_to_file, self.name_of_file, data)
        pass
        
    def go_back(self) -> bool:
        match self.current_page:
            case "csv":
                if self.edit_csv_page.has_changed() and not self.edit_csv_page.quit_without_saving:
                    save_or_quit_year(self.edit_csv_page, self.save_csv, self.go_back)
                else:
                    self.edit_csv_page.quit_without_saving = False
                    self.open_homepage()
                return False
            case "menu":
                self.open_homepage()
                return False
            case "home":
                return True
            case _:
                return True
        
    def open_homepage(self):
        self.current_page = "home"
        self.edit_homepage.show()
        pass
        
    def open_file(self, path_to_file: str, name_of_file: str):
        self.edit_csv_page.close()
        data = read_csv(path_to_file, name_of_file)
        self.edit_csv_page.populate_CSV_frame(name_of_file, data)
        self.path_to_file = path_to_file
        self.name_of_file = name_of_file
        self.current_page = "csv"
        self.edit_csv_page.show()
        pass
        
    def open_data(self):
        self.open_file(path.join(self.path_to_year, "configs"), "data.csv")
        pass
    
    def open_data_content(self):
        self.edit_menu.delete_buttons()
        for path_to_file, name_of_file in find_or_create_data_files(path.join(self.path_to_year, "configs"), "data.csv", path.join(self.path_to_year, "inputs", "data")):
            self.edit_menu.add_button(path_to_file, name_of_file)
        self.current_page = "menu"
        self.edit_menu_page.show()
        pass
    
    def open_targets(self):
        self.edit_menu.delete_buttons()
        for path_to_file, name_of_file in find_or_create_target_files(path.join(self.path_to_year, "configs"), "sub_goals.csv", path.join(self.path_to_year, "inputs", "targets")):
            self.edit_menu.add_button(path_to_file, name_of_file)
        self.current_page = "menu"
        self.edit_menu_page.show()
        pass
    
    def open_configs(self):
        self.open_file(path.join(self.path_to_year, "configs"), "configs.csv")
        pass
    
    def open_goals(self):
        self.open_file(path.join(self.path_to_year, "configs"), "goals.csv")
        pass
    
    def open_sub_goals(self):
        self.open_file(path.join(self.path_to_year, "configs"), "sub_goals.csv")
        pass
    
        
        
class YearPage(Page):
    def __init__(self, master: App, edit_year, create_report, open_report):
        super().__init__(master)
        
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.year_header = ctk.CTkFrame(self)
        self.year_header.grid(row=0, column=0, sticky="new")
        self.year_header.grid_rowconfigure(0, weight=1)
        self.year_header.grid_columnconfigure(0, weight=1)
        self.year_header.grid_columnconfigure(1, weight=1)
        
        self.year_label = ctk.CTkLabel(self.year_header, text="year")
        self.year_label.grid(row=0, column=0, sticky="nw")
        
        self.year_path = ""
        self.comp_year_path = ""
        self.comp_year = 0
        
        self.edit_year_button = ctk.CTkButton(self.year_header, text="Edit Year", command=lambda: edit_year(self.year_path), height=master.button_width, width=master.button_width)
        self.edit_year_button.grid(row=0, column=1, sticky="ne")
        
        self.edit_year_button = ctk.CTkButton(self, text="Create Report", command=lambda: create_report(self.year_label.cget("text"), self.year_path, "Jan"), height=master.button_height) #TODO: Change the Starting Month.
        self.edit_year_button.grid(row=1, column=0, sticky="new")
        
        self.report_scroll_frame = ScrollableButtonFrame(self, open_report)
        self.report_scroll_frame.grid(row=2, column=0, sticky="nsew")

class NewYearPage(Page):
    def __init__(self, master: App, create_year: Callable):
        super().__init__(master)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_propagate(False)

        self.body_frame = ctk.CTkFrame(self)
        self.body_frame.grid(row=0, column=0, sticky="nsew")
        self.body_frame.grid_rowconfigure(0, weight=1)
        self.body_frame.grid_columnconfigure(0, weight=1)
        self.body_frame.grid_columnconfigure(1, weight=1)
        

        self.year_frame = ctk.CTkFrame(self.body_frame)
        self.year_frame.grid(row=0, column=0, sticky="nsew")
        self.year_frame.grid_rowconfigure(0, weight=1)
        self.year_frame.grid_rowconfigure(1, weight=1)
        self.year_frame.grid_columnconfigure(0, weight=1)
        self.year_frame.grid_propagate(False)

        self.select_year_label = ctk.CTkLabel(self.year_frame, text="Please Input the Year (####-####)")
        self.select_year_label.grid(row=0, column=0, sticky="sew")
        
        self.select_year_textbox = ctk.CTkTextbox(self.year_frame, height=80)
        self.select_year_textbox.grid(row=1, column=0, sticky="new")
        self.select_year_textbox.insert("0.0", " ")
        
        self.comp_year_frame = ctk.CTkFrame(self.body_frame)
        self.comp_year_frame.grid(row=0, column=1, sticky="nsew")
        self.comp_year_frame.grid_rowconfigure(0, weight=1)
        self.comp_year_frame.grid_rowconfigure(1, weight=1)
        self.comp_year_frame.grid_columnconfigure(0, weight=1)
        self.comp_year_frame.grid_propagate(False)
        
        self.comp_year_label = ctk.CTkLabel(self.comp_year_frame, text="Please Select a Comparison Year")
        self.comp_year_label.grid(row=0, column=0, sticky="sew")
        
        self.comp_year_dropdown = ctk.CTkOptionMenu(self.comp_year_frame, values=["None"])
        self.comp_year_dropdown.grid(row=1, column=0, sticky="new")
        
        self.create_year_button = ctk.CTkButton(self, height=40, text="Create Year", command=lambda: create_year(self.select_year_textbox.get("0.0", "end-1c"), self.comp_year_dropdown.get()))
        self.create_year_button.grid(row=1, column=0, sticky="sew")

    def initialize_dropdown(self, years: list[str]):
        years.insert(0, "None")
        self.comp_year_dropdown.configure(values=years)
        self.comp_year_dropdown.set("None")

class ReportDraftsPage(Page):
    def __init__(self, master):
        super().__init__(master)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.report_draft_scroll_frame = ScrollableButtonFrame(self, lambda: print()) #TODO: Change command.
        self.report_draft_scroll_frame.grid(row=0, column=0, sticky="nsew")

class SettingsPage(Page):
    def __init__(self, master, path_to_configs: str, go_back: Callable):
        super().__init__(master)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.path_to_configs = path_to_configs
        self.go_back = go_back

        self.settings = CSVFrame(self, self.save)
        self.settings.grid(row=0, column=0, sticky="nsew")
    
    def populate_settings(self, configs: list[list[str]]):
        self.settings.populate_CSV_frame("configs.csv", configs)
    
    def save(self):
        if self.settings.has_changed() and not self.settings.quit_without_saving:
            save_or_quit_year(self.settings, self.save_csv, self.go_back)
            return False
        else:
            self.settings.quit_without_saving = False
            return True
    
    def save_csv(self):
        data = self.settings.save_changes()
        if not data:
            return
        write_csv(self.path_to_configs, "configs.csv", data)

class Homepage(Page):
    def __init__(self, master: App, create_year: Callable, open_year: Callable):
        super().__init__(master)
        
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.create_year_button = ctk.CTkButton(self, text="Create Year", command=create_year, height=master.button_height)
        self.create_year_button.grid(row=0, column=0, sticky="new")

        self.year_scroll_frame = ScrollableButtonFrame(self, open_year)
        self.year_scroll_frame.grid(row=1, column=0, sticky="nsew")
        
class App(ctk.CTk):
    def __init__(self, 
                 get_home_directory: Callable, 
                 path_to_configs: str, 
                 get_years, 
                 get_reports, 
                 create_years, 
                 create_reports):
        super().__init__()
        
        self.get_home_directory = get_home_directory
        self.path_to_configs = path_to_configs
        self.get_years = get_years
        self.get_reports = get_reports
        self.create_years = create_years
        self.create_reports = create_reports
        self.configure_app()
        
        self.geometry("500x500")
        self.minsize(width=500, height=500)
        self.title("KPI Dashboard")
        self.iconbitmap(self.get_home_directory(path.join("static", "LSM.ico")))
        
            # Two Rows, One Column. Column expands horizontally. Only the bottom Row expands vertically.
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        
        
            # Header.
        self.header = ctk.CTkFrame(self, height=self.button_height)
        self.header.grid(row=0, column=0, sticky="nsew")
        self.header.grid_rowconfigure(0, weight=1)
        self.header.grid_columnconfigure(0, weight=1)
        self.header.grid_columnconfigure(1, weight=1)
        self.header.grid_propagate(False)
        
        
            # Control Buttons Frame.
        self.control_buttons_frame = ctk.CTkFrame(self.header)
        self.control_buttons_frame.grid(row=0, column=1, sticky="nsew")
        
            # Control Buttons Pages.
        
            # Not Home.
        self.not_home_control_page = Page(self.control_buttons_frame)
        self.not_home_control_page.grid_rowconfigure(0, weight=1)
        self.not_home_control_page.grid_columnconfigure(0, weight=1)
            # Go Home Button.
        self.go_home_button = ctk.CTkButton(self.not_home_control_page, text="Go Home", command=lambda: self.open_page("home"), height=self.button_height, width=self.button_width)
        self.go_home_button.grid(row=0, column=0, sticky="e")
            # Place the Page.
        self.not_home_control_page.place(in_=self.control_buttons_frame, x=0, y=0, relwidth=1, relheight=1)
        
            # On Home.
        self.on_home_control_page = Page(self.control_buttons_frame)
        self.on_home_control_page.grid_rowconfigure(0, weight=1)
        self.on_home_control_page.grid_columnconfigure(0, weight=1)
            # Report Drafts Button.
        # self.report_drafts_button = ctk.CTkButton(self.on_home_control_page, text="Report Drafts", command=lambda: self.open_page("draft"), height=button_height, width=button_width)
        # self.report_drafts_button.grid(row=0, column=0, sticky="e")
            # Place the Page.
        self.on_home_control_page.place(in_=self.control_buttons_frame, x=0, y=0, relwidth=1, relheight=1)
        
        
            # Settings Frame.
        self.settings_button_frame = ctk.CTkFrame(self.header)
        self.settings_button_frame.grid(row=0, column=0, sticky="nsew")
        self.settings_button_frame.grid_rowconfigure(0, weight=1)
        self.settings_button_frame.grid_columnconfigure(0, weight=0)
        self.settings_button_frame.grid_columnconfigure(1, weight=0)
        
            # Go Back Button.
        self.go_back_button = ctk.CTkButton(self.settings_button_frame, text="Go Back", command=self.back_page, height=self.button_height, width=self.button_width)
        self.go_back_button.grid(row=0, column=0, sticky="w")
        
            # Settings Button.
        self.settings_button = ctk.CTkButton(self.settings_button_frame, text="Settings", command=self.open_settings, height=self.button_height, width=self.button_width) #TODO: Change command.
        self.settings_button.grid(row=0, column=1, sticky="w")



            # Body.
        self.body = ctk.CTkFrame(self)
        self.body.grid(row=1, column=0, sticky="nsew")
        
            # Body Pages.
        self.body_pages = {}
        self.current_page = ""
        self.i = 0
        
            # Homepage.
        self.body_pages["home"] = Homepage(self, self.open_new_year, self.open_year)
        
        self.body_pages["settings"] = SettingsPage(self, self.path_to_configs, self.back_page)
        
        # self.body_pages["home"].place(in_=self.body, x=0, y=0, relwidth=1, relheight=1)
        
            #Report Draft Page.
        # self.body_pages["drafts"] = ReportDraftsPage(self)
        # self.body_pages["drafts"].place(in_=self.body, x=0, y=0, relwidth=1, relheight=1)
        
        self.body_pages["new_year"] = NewYearPage(self, self.create_year)
        
        self.body_pages["edit_year"] = EditYearPage(self)
        
        self.body_pages["year"] = YearPage(self, self.open_edit_year, self.open_new_report, self.open_report)
        # self.body_pages["year"].place(in_=self.body, x=0, y=0, relwidth=1, relheight=1)


        self.body_pages["new_report"] = NewReportPage(self, self.create_report)
        
        self.body_pages["version_select"] = ReportSelection(self, self.open_report_helper)
        
        self.body_pages["report_validation"] = ReportValidationPage(self, self.create_graph)
        
        for key in self.body_pages:
            self.body_pages[key].place(in_=self.body, x=0, y=0, relwidth=1, relheight=1)
        
        
        self.start_home()
    
    def configure_app(self):
        self.configs = read_csv(self.path_to_configs, "configs.csv")
        self.home_directory = self.get_home_directory(self.configs[find_row(self.configs, "home_directory")][1])
        self.button_height = int(self.configs[find_row(self.configs, "button_height")][1])
        self.button_width = int(self.configs[find_row(self.configs, "button_width")][1])
        self.comp_year_color = self.configs[find_row(self.configs, "comp_year_color")][1]
        self.target_color = self.configs[find_row(self.configs, "target_color")][1]
        self.year_color = self.configs[find_row(self.configs, "year_color")][1]
    
    def create_year(self, year: str, comp_year: str):
        
        year = year.strip()
        if not self.create_years(self.home_directory, year, comp_year):
            return

        self.start_home()
    
    def create_report(self, path_to_year: str, month: str):
        
        if not self.create_reports(path_to_year, month):
            return
        self.start_home()
    
    def start_home(self):
        self.body_pages["home"].year_scroll_frame.delete_buttons()
        self.body_pages["home"].year_scroll_frame.add_buttons(self.get_years(self.home_directory))
        self.open_page("home")

    def open_new_year(self):
        years = self.get_years(self.home_directory)
        self.body_pages["new_year"].initialize_dropdown([year for year, year_path in years])
        self.open_page("new_year")
        
    def open_edit_year(self, year_path):
        self.body_pages["edit_year"].initialize(year_path)
        self.open_page("edit_year")

    def open_settings(self):
        configs = read_csv(self.path_to_configs, "configs.csv")
        self.body_pages["settings"].populate_settings(configs)
        self.open_page("settings")
    
    def open_year(self, year_path, year):
        
        self.body_pages["year"].report_scroll_frame.delete_buttons()
        self.body_pages["year"].year_label.configure(text=year)
        self.body_pages["year"].year_path = year_path
        # print(year_path, self.i)
        self.i += 1
        # print(path.join(year_path, "configs"), self.i)
        self.i += 1
        
        year_configs = read_csv(path.join(year_path, "configs"), "configs.csv")
        # print(year_configs, self.i)
        self.i += 1
        comp_year = year_configs[find_row(year_configs, "comp_year")][1]
        comp_year_path = ""
        if comp_year != "None":
            years = self.get_years(self.home_directory)
            for year in years:
                if year[0] == comp_year:
                    comp_year_path = year[1]
                    break
            self.body_pages["year"].comp_year = int(comp_year.split("-")[1])
            self.body_pages["year"].comp_year_path = comp_year_path
        self.body_pages["year"].report_scroll_frame.add_buttons(self.get_reports(year_path))
        self.open_page("year")

    def open_new_report(self, year, path_to_year, month):
        self.body_pages["new_report"].initialize(year, path_to_year, month)
        self.open_page("new_report")
        
    def open_report_version_select(self, report_path, versions, month):
        self.body_pages["version_select"].report_selection(report_path, versions, month)
        self.open_page("version_select")
        
        
    def open_report(self, report_path, report):
        
        # print(report_path)
        configs_path = path.join(report_path, "configs")
        configs = read_csv(configs_path, "configs.csv")
        
        versions: list[str] = helper(configs[find_row(configs, "versions")][1])
        # print(versions)
        month: str = configs[find_row(configs, "month")][1]
        if not versions:
            self.open_report_helper(report_path, "1", month)
            return
        self.open_report_version_select(report_path, versions, month)
        
        

    def open_report_helper(self, report_path, version, month):
        
        if version == "Create New":
            version = new_report_version(report_path)
        
        months = {"Jul": 7, 
            "Aug": 8, 
            "Sep": 9, 
            "Oct": 10, 
            "Nov": 11, 
            "Dec": 12, 
            "Jan": 1, 
            "Feb": 2, 
            "Mar": 3, 
            "Apr": 4, 
            "May": 5, 
            "Jun": 6}
        

        
        year_path = self.body_pages["year"].year_path
        year = self.body_pages["year"].year_label.cget("text").split("-")
        self.body_pages["report_validation"].create_report(
            report_path,
            version, 
            year_path,
            year, 
            months[month],
            int(year[-1]),
            self.body_pages["year"].comp_year,
            self.body_pages["year"].comp_year_path)
        self.body_pages["report_validation"].generate_sub_goal()
        
        self.open_page("report_validation")
        

        
        # print(report, path)
        
        # self.body_pages["report"].report_scroll_frame.delete_buttons()
        # self.body_pages["report"].year_label.configure(text=report)
        
        # reports = self.get_reports(path)
        # if reports != 0:
        #     for report, report_path in reports:
        #         self.body_pages["report"].report_scroll_frame.add_button(report, report_path)
        # self.open_page("report")
        pass
    def back_page(self):
        match self.current_page:
            case "home":
                pass
            case "year":
                self.open_page("home")
            case "report_draft":
                self.open_page("home")
            case "settings":
                if self.body_pages["settings"].save():
                    self.configure_app()
                    self.start_home()
            case "new_report":
                self.open_page("year")
            case "edit_year":
                if self.body_pages["edit_year"].go_back():
                    self.open_page("year")
            case "report_validation":
                if self.body_pages["report_validation"].data_active:
                    if self.body_pages["report_validation"].has_changed() and not self.body_pages["report_validation"].override_quit:
                        save_or_quit(self.body_pages["report_validation"], self.back_page)
                    else:
                        self.body_pages["report_validation"].close_data()
                else:
                    self.open_year(self.body_pages["report_validation"].path_to_year, self.body_pages["year"].year_label.cget("text"))
                # if self.body_pages["report_validation"].is_saved:
                #     pass
                # else:
                #     #TODO: Prompt user to save report draft.
                #     pass
    
    def open_page(self, page_name: str):
        self.body_pages[page_name].show()
        self.current_page = page_name
        if page_name == "home":
            self.on_home_control_page.show()
        else:
            self.not_home_control_page.show()

    def create_graph(self,
                 sub_goal: str,
                 summed_column: str, 
                 current_year: int, 
                 year_data: list[float], 
                 target_data: list[float], 
                 path_to_report: str, 
                 comp_year_data: list[float] = [], 
                 comp_year: int = 0,
                 affix: str = "") -> str:
        year = ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        
        fig = Figure()
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        ax.set_ylabel(summed_column)
        ncols = 2
        if comp_year_data:
            ax.plot(year[:len(comp_year_data)], comp_year_data, marker="o", label=comp_year, color=self.comp_year_color)
            ncols += 1
        ax.plot(year[:len(target_data)], target_data, marker="o", label=f"{current_year} Target", color=self.target_color)
        ax.plot(year[:len(year_data)], year_data, marker="o", label=f"{current_year} Actual", color=self.year_color)
        ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncols=ncols, mode="expand", borderaxespad=0.)
        canvas.draw()
        fig.savefig(f"{path_to_report}/outputs/graphs/{sub_goal}{affix}_graph.png")
        return f"{path_to_report}/outputs/graphs/{sub_goal}{affix}_graph.png"
    

def save_or_quit(csv: ReportValidationPage, quit: Callable):
        def quit_without_saving():
            save_or_quit_window.destroy()
            csv.override_quit = True
            quit()
        def quit_with_saving():
            save_or_quit_window.destroy()
            csv.save_csv()
            quit()
        save_or_quit_window = ctk.CTkToplevel()
        save_or_quit_window.geometry("300x300")
        save_or_quit_window.title("Unsaved Changes")
        save_or_quit_window.resizable(False, False)
        save_or_quit_window.grab_set()
        
        save_or_quit_window.grid_rowconfigure(0, weight=1)
        save_or_quit_window.grid_rowconfigure(1, weight=1)
        
        unsaved_changes_label = ctk.CTkLabel(save_or_quit_window, text="You have unsaved changes.\nWould you like to save and exist, or exist without saving?")
        unsaved_changes_label.grid(row=0, column=0, sticky="nsew")
        
        buttons_frame = ctk.CTkFrame(save_or_quit_window)
        buttons_frame.grid(row=1, column=0, sticky="nsew")
        buttons_frame.grid_rowconfigure(0, weight=0)
        buttons_frame.grid_columnconfigure(0, weight=0)
        buttons_frame.grid_columnconfigure(1, weight=0)
        
        quit_button = ctk.CTkButton(buttons_frame, text="Exit Without Saving", command=quit_without_saving)
        quit_button.grid(row=0, column=0, sticky="w")
        
        save_button = ctk.CTkButton(buttons_frame, text="Save and Exit", command=quit_with_saving)
        save_button.grid(row=0, column=1, sticky="e")
        
def save_or_quit_year(csv: CSVFrame, save: Callable, quit: Callable):
        def quit_without_saving():
            save_or_quit_window.destroy()
            csv.quit_without_saving = True
            quit()
        def quit_with_saving():
            save_or_quit_window.destroy()
            save()
            quit()
        save_or_quit_window = ctk.CTkToplevel()
        save_or_quit_window.geometry("300x300")
        save_or_quit_window.title("Unsaved Changes")
        save_or_quit_window.resizable(False, False)
        save_or_quit_window.grab_set()
        
        save_or_quit_window.grid_rowconfigure(0, weight=1)
        save_or_quit_window.grid_rowconfigure(1, weight=1)
        
        unsaved_changes_label = ctk.CTkLabel(save_or_quit_window, text="You have unsaved changes.\nWould you like to save and exist, or exist without saving?")
        unsaved_changes_label.grid(row=0, column=0, sticky="nsew")
        
        buttons_frame = ctk.CTkFrame(save_or_quit_window)
        buttons_frame.grid(row=1, column=0, sticky="nsew")
        buttons_frame.grid_rowconfigure(0, weight=0)
        buttons_frame.grid_columnconfigure(0, weight=0)
        buttons_frame.grid_columnconfigure(1, weight=0)
        
        quit_button = ctk.CTkButton(buttons_frame, text="Exit Without Saving", command=quit_without_saving)
        quit_button.grid(row=0, column=0, sticky="w")
        
        save_button = ctk.CTkButton(buttons_frame, text="Save and Exit", command=quit_with_saving)
        save_button.grid(row=0, column=1, sticky="e")
        
def save_or_quit_goal(goal: GoalFrame, save: Callable, quit: Callable):
        def quit_without_saving():
            save_or_quit_window.destroy()
            quit(True)
        def quit_with_saving():
            save_or_quit_window.destroy()
            save()
            quit() 
        save_or_quit_window = ctk.CTkToplevel()
        save_or_quit_window.geometry("300x300")
        save_or_quit_window.title("Unsaved Changes")
        save_or_quit_window.resizable(False, False)
        save_or_quit_window.grab_set()
        
        save_or_quit_window.grid_rowconfigure(0, weight=1)
        save_or_quit_window.grid_rowconfigure(1, weight=1)
        
        unsaved_changes_label = ctk.CTkLabel(save_or_quit_window, text="You have unsaved changes.\nWould you like to save and exist, or exist without saving?")
        unsaved_changes_label.grid(row=0, column=0, sticky="nsew")
        
        buttons_frame = ctk.CTkFrame(save_or_quit_window)
        buttons_frame.grid(row=1, column=0, sticky="nsew")
        buttons_frame.grid_rowconfigure(0, weight=0)
        buttons_frame.grid_columnconfigure(0, weight=0)
        buttons_frame.grid_columnconfigure(1, weight=0)
        
        quit_button = ctk.CTkButton(buttons_frame, text="Exit Without Saving", command=quit_without_saving)
        quit_button.grid(row=0, column=0, sticky="w")
        
        save_button = ctk.CTkButton(buttons_frame, text="Save and Exit", command=quit_with_saving)
        save_button.grid(row=0, column=1, sticky="e")
def log(log: str):
    pass
