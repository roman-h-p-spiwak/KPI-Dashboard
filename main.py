from modules.directory_management import year_create, report_create, year_index, report_index, get_app_configs, resource_path
from modules.inputs import find_row, find_column
from modules.gui import App


CONFIGS = get_app_configs(resource_path(), "configs.csv")
print(resource_path(CONFIGS[find_row(CONFIGS, "home_directory")][1]))
HOME_DIRECTORY = resource_path(CONFIGS[find_row(CONFIGS, "home_directory")][1])

def create_years(year: str, comp_year: str):
    
    if not year_create(HOME_DIRECTORY, year, comp_year):
        return

    year_index(HOME_DIRECTORY)

    pass




def main():

    
    app = App(HOME_DIRECTORY, 
              int(CONFIGS[find_row(CONFIGS, "button_height")][1]), 
              int(CONFIGS[find_row(CONFIGS, "button_width")][1]), 
              year_index, 
              report_index, 
              year_create, 
              report_create)
    app.mainloop()


if __name__ == "__main__":
    main()