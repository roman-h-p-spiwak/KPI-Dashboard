from modules.directory_management import year_create, report_create, year_index, report_index, get_app_configs
from modules.inputs import find_row, find_column
from modules.gui import App

CONFIGS = "./configs.csv"
configs = get_app_configs(CONFIGS)
home_directory = configs[find_row(configs, "home_directory")][1]

def create_years(year: str, comp_year: str):
    
    if not year_create(home_directory, year, comp_year):
        return

    year_index(home_directory)

    pass


def main():

    
    app = App(home_directory, 
              int(configs[find_row(configs, "button_height")][1]), 
              int(configs[find_row(configs, "button_width")][1]), 
              year_index, 
              report_index, 
              year_create, 
              report_create)
    app.mainloop()


if __name__ == "__main__":
    main()