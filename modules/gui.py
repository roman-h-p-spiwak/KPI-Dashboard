import customtkinter as ctk
import directory_management as dm

BUTTON_HEIGHT = 40
BUTTON_WIDTH = 40

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
        self.buttons.clear()
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


class YearPage(Page):
    def __init__(self, master, year):
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
        
        self.year_label = ctk.CTkLabel(self.year_header, text=year)
        self.year_label.grid(row=0, column=0, sticky="nw")
        
        self.edit_year_button = ctk.CTkButton(self.year_header, text="Edit Year", command=lambda: print("Edited Year"), height=BUTTON_HEIGHT, width=BUTTON_WIDTH) #TODO: Change command.
        self.edit_year_button.grid(row=0, column=1, sticky="ne")
        
        self.edit_year_button = ctk.CTkButton(self, text="Create Report", command=lambda: print("Created Report"), height=BUTTON_HEIGHT) #TODO: Change command.
        self.edit_year_button.grid(row=1, column=0, sticky="new")  
        
        self.report_scroll_frame = ScrollableButtonFrame(self, print) #TODO: Change command.
        self.report_scroll_frame.grid(row=2, column=0, sticky="nsew")


class Homepage(Page):
    def __init__(self, master, open_year):
        super().__init__(master)
        
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.create_year_button = ctk.CTkButton(self, text="Create Year", command=lambda: print("Created Year"), height=BUTTON_HEIGHT) #TODO: Change command.
        self.create_year_button.grid(row=0, column=0, sticky="new")

        self.year_scroll_frame = ScrollableButtonFrame(self, open_year) #TODO: Change command.
        self.year_scroll_frame.grid(row=1, column=0, sticky="nsew")
        

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.geometry("500x500")
        self.minsize(width=500, height=500)
        self.title("CTk example")
        
            # Two Rows, One Column. Column expands horizontally. Only the bottom Row expands vertically.
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        
        
            # Header.
        self.header = ctk.CTkFrame(self, height=BUTTON_HEIGHT)
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
        self.go_home_button = ctk.CTkButton(self.not_home_control_page, text="Go Home", command=lambda: self.open_page("home"), height=BUTTON_HEIGHT, width=BUTTON_WIDTH)
        self.go_home_button.grid(row=0, column=0, sticky="e")
            # Place the Page.
        self.not_home_control_page.place(in_=self.control_buttons_frame, x=0, y=0, relwidth=1, relheight=1)
        
            # On Home.
        self.on_home_control_page = Page(self.control_buttons_frame)
        self.on_home_control_page.grid_rowconfigure(0, weight=1)
        self.on_home_control_page.grid_columnconfigure(0, weight=1)
            # Report Drafts Button.
        self.report_drafts_button = ctk.CTkButton(self.on_home_control_page, text="Report Drafts", command=lambda: self.open_page("draft"), height=BUTTON_HEIGHT, width=BUTTON_WIDTH)
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
        self.go_back_button = ctk.CTkButton(self.settings_button_frame, text="Go Back", command=self.back_page, height=BUTTON_HEIGHT, width=BUTTON_WIDTH)
        self.go_back_button.grid(row=0, column=0, sticky="w")
        
            # Settings Button.
        self.settings_button = ctk.CTkButton(self.settings_button_frame, text="Settings", command=lambda: print("Opened Settings"), height=BUTTON_HEIGHT, width=BUTTON_WIDTH) #TODO: Change command.
        self.settings_button.grid(row=0, column=1, sticky="w")



            # Body.
        self.body = ctk.CTkFrame(self)
        self.body.grid(row=1, column=0, sticky="nsew")
        
            # Body Pages.
        self.body_pages = {}
        self.body_pages_order = []  #TODO: Explain why.
        
            # Homepage.
        self.body_pages["home"] = Homepage(self, self.start_year)
        self.body_pages_order.append("home")
        self.body_pages["home"].place(in_=self.body, x=0, y=0, relwidth=1, relheight=1)
        
            #Report Draft Page.
        self.body_pages["draft"] = ReportDraftPage(self)
        self.body_pages_order.append("draft")
        self.body_pages["draft"].place(in_=self.body, x=0, y=0, relwidth=1, relheight=1)
        

        
        
        self.start_home()
    
    def start_home(self):
        for year, path in dm.year_index(HOME_DIRECTORY):
            self.body_pages["home"].year_scroll_frame.add_button(year, path)
        self.open_page("home")
                    
    def start_year(self, year, path):
        if year not in self.body_pages:        
                #Year Page.
            self.body_pages[year] = YearPage(self, year)
            self.body_pages_order.insert(0, year)
            
            for report, report_path in dm.report_index(path):
                self.body_pages[year].report_scroll_frame.add_button(report, report_path)
            
            self.body_pages[year].place(in_=self.body, x=0, y=0, relwidth=1, relheight=1)
            
        self.open_page(year)
        
    
    def open_page(self, page_name):
        self.body_pages[page_name].show()
        index = self.body_pages_order.index(page_name)
        self.body_pages_order[index], self.body_pages_order[0] = self.body_pages_order[0], self.body_pages_order[index]
        
        self.header_control()
    
    def back_page(self):
        self.body_pages_order[1], self.body_pages_order[0] = self.body_pages_order[0], self.body_pages_order[1]
        self.body_pages[self.body_pages_order[0]].show()
        
        self.header_control()
            
    def header_control(self):
        if self.body_pages_order[0] == "home":
            self.on_home_control_page.show()
        else:
            self.not_home_control_page.show()
            
            

# This is for testing.          
app = App()
app.mainloop()