from __future__ import annotations
import customtkinter as ctk

HOME_DIRECTORY = "../.testdata/"

class ScrollableButtonFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, open_object):
        super().__init__(master)
        
        self.grid_columnconfigure(0, weight=1)
        self.open_object = open_object
        self.num_buttons = 0
        self.buttons = []
        
    def add_button(self, name, path):
        new_button = ctk.CTkButton(self, text=name, command=lambda: self.open_object(name, path))
        new_button.grid(row=self.num_buttons, column=0, padx=10, pady=10, sticky="ew")        
        self.buttons.append(new_button)
        self.num_buttons += 1
        
    def delete_buttons(self):
        while len(self.buttons) > 0:
            button = self.buttons.pop(0)
            button.destroy()
        self.num_buttons = 0
   
class Page(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
    def show(self):
        self.lift()
   
   
class ReportDraftPage(Page):
    def __init__(self, master):
        super().__init__(master)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.report_draft_scroll_frame = ScrollableButtonFrame(self, lambda: print()) #TODO: Change command.
        self.report_draft_scroll_frame.grid(row=0, column=0, sticky="nsew")


class EditYearPage(Page):
    def __init__(self, master: App, year):
        super().__init__(master)
        
        
        
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
        
        self.edit_year_button = ctk.CTkButton(self.year_header, text="Edit Year", command=lambda: edit_year(self.year_label.cget("text")), height=master.button_width, width=master.button_width)
        self.edit_year_button.grid(row=0, column=1, sticky="ne")
        
        self.edit_year_button = ctk.CTkButton(self, text="Create Report", command=lambda: create_report(self.year_label.cget("text")), height=master.button_height)
        self.edit_year_button.grid(row=1, column=0, sticky="new")
        
        self.report_scroll_frame = ScrollableButtonFrame(self, open_report)
        self.report_scroll_frame.grid(row=2, column=0, sticky="nsew")


class Homepage(Page):
    def __init__(self, master: App, open_year):
        super().__init__(master)
        
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.create_year_button = ctk.CTkButton(self, text="Create Year", command=lambda: print("Created Year"), height=master.button_height) #TODO: Change command.
        self.create_year_button.grid(row=0, column=0, sticky="new")

        self.year_scroll_frame = ScrollableButtonFrame(self, open_year)
        self.year_scroll_frame.grid(row=1, column=0, sticky="nsew")
        

class App(ctk.CTk):
    def __init__(self, 
                 home_directory: str, 
                 button_height: int, 
                 button_width: int, 
                 get_years, 
                 get_reports, 
                 create_years, 
                 create_reports):
        super().__init__()
        
        self.home_directory = home_directory
        self.button_height = button_height
        self.button_width = button_width
        self.get_years = get_years
        self.get_reports = get_reports
        self.create_years = create_years
        self.create_reports = create_reports
        
        self.geometry("500x500")
        self.minsize(width=500, height=500)
        self.title("CTk example")
        
            # Two Rows, One Column. Column expands horizontally. Only the bottom Row expands vertically.
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        
        
            # Header.
        self.header = ctk.CTkFrame(self, height=button_height)
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
        self.go_home_button = ctk.CTkButton(self.not_home_control_page, text="Go Home", command=lambda: self.open_page("home"), height=button_height, width=button_width)
        self.go_home_button.grid(row=0, column=0, sticky="e")
            # Place the Page.
        self.not_home_control_page.place(in_=self.control_buttons_frame, x=0, y=0, relwidth=1, relheight=1)
        
            # On Home.
        self.on_home_control_page = Page(self.control_buttons_frame)
        self.on_home_control_page.grid_rowconfigure(0, weight=1)
        self.on_home_control_page.grid_columnconfigure(0, weight=1)
            # Report Drafts Button.
        self.report_drafts_button = ctk.CTkButton(self.on_home_control_page, text="Report Drafts", command=lambda: self.open_page("draft"), height=button_height, width=button_width)
        self.report_drafts_button.grid(row=0, column=0, sticky="e")
            # Place the Page.
        self.on_home_control_page.place(in_=self.control_buttons_frame, x=0, y=0, relwidth=1, relheight=1)
        
        
            # Settings Frame.
        self.settings_button_frame = ctk.CTkFrame(self.header)
        self.settings_button_frame.grid(row=0, column=0, sticky="nsew")
        self.settings_button_frame.grid_rowconfigure(0, weight=1)
        self.settings_button_frame.grid_columnconfigure(0, weight=0)
        self.settings_button_frame.grid_columnconfigure(1, weight=0)
        
            # Go Back Button.
        self.go_back_button = ctk.CTkButton(self.settings_button_frame, text="Go Back", command=self.back_page, height=button_height, width=button_width)
        self.go_back_button.grid(row=0, column=0, sticky="w")
        
            # Settings Button.
        self.settings_button = ctk.CTkButton(self.settings_button_frame, text="Settings", command=lambda: print("Opened Settings"), height=button_height, width=button_width) #TODO: Change command.
        self.settings_button.grid(row=0, column=1, sticky="w")



            # Body.
        self.body = ctk.CTkFrame(self)
        self.body.grid(row=1, column=0, sticky="nsew")
        
            # Body Pages.
        self.body_pages = {}
        self.current_page = ""
        
            # Homepage.
        self.body_pages["home"] = Homepage(self, self.open_year)
        # self.body_pages["home"].place(in_=self.body, x=0, y=0, relwidth=1, relheight=1)
        
            #Report Draft Page.
        self.body_pages["draft"] = ReportDraftPage(self)
        # self.body_pages["draft"].place(in_=self.body, x=0, y=0, relwidth=1, relheight=1)
        
        self.body_pages["year"] = YearPage(self, print, print, print)
        # self.body_pages["year"].place(in_=self.body, x=0, y=0, relwidth=1, relheight=1)

        
        for key in self.body_pages:
            self.body_pages[key].place(in_=self.body, x=0, y=0, relwidth=1, relheight=1)
        
        
        self.start_home()
    
    def start_home(self):
        years = self.get_years(self.home_directory)
        if years != 0:
            for year, path in years:
                self.body_pages["home"].year_scroll_frame.add_button(year, path)
        self.open_page("home")
                    
    def open_year(self, year, path):
        
        self.body_pages["year"].report_scroll_frame.delete_buttons()
        self.body_pages["year"].year_label.configure(text=year)
        
        reports = self.get_reports(path) #TODO: Just add from the list.
        if reports != 0:
            for report, report_path in reports:
                self.body_pages["year"].report_scroll_frame.add_button(report, report_path)
        self.open_page("year")

    def open_report(self, report, path):
        
        print(report, path)
        
        # self.body_pages["report"].report_scroll_frame.delete_buttons()
        # self.body_pages["report"].year_label.configure(text=report)
        
        # reports = self.get_reports(path)
        # if reports != 0:
        #     for report, report_path in reports:
        #         self.body_pages["report"].report_scroll_frame.add_button(report, report_path)
        # self.open_page("report")

    def back_page(self):
        match self.current_page:
            case "home":
                pass
            case "year":
                self.open_page("home")
            case "report_draft":
                self.open_page("home")
            case "settings":
                self.body_pages["settings"].save()
                self.open_page("home")
            case "new_report":
                self.open_page("year")
            case "report_validation":
                if self.body_pages["report_validation"].is_saved:
                    self.open_year("year", self.body_pages["report_validation"].year_path)
                else:
                    #TODO: Prompt user to save report draft.
                    pass
    
    def open_page(self, page_name: str):
        self.body_pages[page_name].show()
        self.current_page = page_name
        if page_name == "home":
            self.on_home_control_page.show()
        else:
            self.not_home_control_page.show()