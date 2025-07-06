# SCRUM

## Overview

The KPI Dashboard is a project for my summer internship at Leadership Southern Maryland. This internship is divided into three separate projects, with each project being one two-week sprint. The intent is to provide the interns with experience using the scrum development framework. The KPI Dashboard project is my second sprint.

This is my first attempt a scrum board at all, let alone one for a real project. Any confusion, misunderstanding, or inefficiencies are certainly do to my inexperience, but the best way to learn is by doing. And the only way to begin is by beginning.

## EPIC - Key Performance Indicator (KPI) Dashboard

Key Performance Indicator Dashboard automated program for Leadership Southern Maryland (LSM).

The KPI Dashboard is made up of three goals with twenty-two sub-goals between them. The data that makes up these goals and sub-goals comes from a variety of places. Some can have an automated data download; others require manual input.

This program is designed to automate that which can be easily automated while providing the user with the ability to easily input manual data. The data is to be stored in offline .csv files with the intent that if the program should break, the data would not be lost.

**Definition of Done:** The application exists as an executable that displays a human usable GUI, allowing the user to create new years, new reports, save and load drafts of reports, input data, modify data, and generate a PDF of the report.

**Time:** The due date is Tuesday, June 15th. It might take up to ...

**As a stakeholder,** **I want** an application that speeds up the monthly process of downloading, formatting, and inserting data to create a KPI Dashboard report, **so that** I can do more with less time, tedium, and bother.

### Accepting Incorrect Usage

The KPI Dashboard project is intended to be completed within one, two-week sprint. Logistically, this makes this project more like a singular story than something large enough to be considered an epic.

However, for the sake of a learning environment, and expanding my abilities, we're going to make the project one epic, and each user story should take a varied amount of time. Therefore, I am most likely using the scrum development framework incorrectly. I accept that as getting used to these terms is something worthwhile in its own right.

## User Stories

I will attempt to set up the user stories following [this](https://www.atlassian.com/agile/project-management/user-stories) website's guide to user stories.

The general format goes:

**Definition of Done:** What done looks like.

**Time:** How long it should take to finish the user story.

**As a {blank},** **I want** something, **so that** it works.

### List of User Stories

- [ ] [Set Up SCRUM Board](#set-up-scrum-board)
- [ ] [Write Documentation](#write-documentation)
- [ ] [API Input](#api-input)
- [ ] [CSV Input](#csv-input)
- [ ] [CSV Output](#csv-output)
- [ ] [Directory Management](#directory-management)
- [ ] [Year Management](#year-management)
- [ ] [Report Management](#report-management)
- [ ] [Data Visualization](#data-visualization)
- [ ] [Data Modification](#data-modification)
- [ ] [Report Finalization](#report-finalization)
- [ ] [Render Data](#render-data)
- [ ] [GUI](#gui)
- [ ] [Homepage](#homepage)
- [ ] [Settings Page](#settings-page)
- [ ] [Report Draft Page](#report-draft-page)
- [ ] [New Year Page](#new-year-page)
- [ ] [Year Page](#year-page)
- [ ] [Edit Year Page](#edit-year-page)
- [ ] [New Report Page](#new-report-page)
- [ ] [Report Validation Page](#report-validation-page)

## Set Up SCRUM Board

**Definition of Done:** The board is set up with the accurate number of user stories and tasks, each describing a distinct feature of the project and the general, granular approach the developer will take to complete said feature.

**Time:** This is going to take a while, and it will probably be finished as the project is getting finished in general

**As a developer,** **I want** to have a general map and overview of the tasks moving forward with this project, **so that** I can fully understand the project, the requirements, and the timeline.

**As a stakeholder,** **I want** to have this document, **so that** I can accurately predict what features will exist in this project, and the estimated time it would take to be completed.

### Set Up SCRUM Board - Tasks

- [X] [Determine KPI Dashboard Specifics](#determine-kpi-dashboard-specifics)
- [ ] [User Story per Major Feature](#user-story-per-major-feature)
- [x] [Finish Epic](#finish-epic)

### Determine KPI Dashboard Specifics

- [x] Read through the previous KPI Dashboards.
- [x] Read through the set up guide for KPI Dashboards.
- [x] Read through the raw data used for KPI Dashboards.
- [x] Write a document explaining my understanding of KPI Dashboards.

### User Story per Major Feature

- [x] Formulate a rough draft plan for the entire project.
- [x] Create the user stories related to the Input.
- [ ] Create the tasks related to the Input.
- [ ] Create the sub-tasks related to the Input.
- [x] Create the user stories related to the Calculation.
- [ ] Create the tasks related to the Calculation.
- [ ] Create the sub-tasks related to the Calculation.
- [x] Create the user stories related to the Output.
- [x] Create the tasks related to the Output.
- [ ] Create the sub-tasks related to the Output.
- [x] Create the user stories related to the GUI.
- [ ] Create the tasks related to the GUI.
- [ ] Create the sub-tasks related to the GUI.

### Finish Epic

- [x] Write the rest of the epic, explaining the project, its goals, and what done looks like.

## Write Documentation

**Definition of Done:** The entire project has simple and easy to read documentation files. Each code file is well-commented, with each class, function, and file having a simple description of what it does and why.

**Time:** This will take as long as the entire project and probably a little longer after that.

**As a developer,** **I want** proper documentation and well-commented code, **so that** future developers, including myself, can easily understand what each part of the program is doing, why, and how it connects to the whole.

**As a stakeholder,** **I want** the program to be well documented, **so that** if something breaks in the future, someone could easily figure out what and how to fix it.

### Write Documentation - Tasks

- [ ] [Good Documentation Practices]
- [ ] []

## API Input

**Definition of Done:** The application is capable of using various API keys to download information related to the month and year of a specific report.

**Time:** This could take a while, depending on which APIs (take, for instance, counting messages on Facebook).

**As a stakeholder,** **I want** as many aspects of the program that can be automated to be automated, **so that** it can save me time.

### API Input - Tasks

## CSV Input

**Definition of Done:** The application is capable of reading in every aspect of every piece of data for every sub-goal purely from .csv files. This ranges from yearly targets, to annual data, to monthly data, to every single piece of data that gets stored in the report's folder after report finalization.

**Time:** This shouldn't take longer than a few hours.

**As a stakeholder,** **I want** to make sure that if something changes with the APIs, the program can work using pure .csv files, **so that** it doesn't become utterly useless.

### CSV Input - Tasks

## CSV Output

**Definition of Done:** The application is capable of offloading data, taken both from APIs and the user input, into .csv files. These .csv files should be the same ones that it is loading data from, and it should be capable of loading data to these files without corruption or duplication.

**Time:** This shouldn't take longer than a few hours.

**As a stakeholder,** **I want** the changes made to data, both from APIs and my input, to be saved to the offline files, **so that** I can see, at any point in the future, exactly what data was used to generate which report, even if the data from the API changes.

### CSV Output - Tasks

## Directory Management

**Definition of Done:** The application has the ability to index all years and months in the set directory. The application has the ability to create new directories for new years, along with their inputs, and months, along with their inputs and outputs. The application has the ability to change the home directory.

**Time:** This should only take a few hours.

**As a stakeholder,** **I want** the application to be able to create and find all the years and months created by the application and change the location where they are saved, **so that** I can use the application to manage the monthly KIP Dashboard reports.

### Directory Management - Tasks

- [ ] [Config Read-In](#config-read-in)
- [ ] [CSV Data Format](#csv-data-format)
- [ ] [In-RAM Data Object](#in-ram-data-object)
- [ ] [In-RAM Year Object](#in-ram-year-object)
- [ ] [In-RAM Report Object](#in-ram-report-object)
- [x] [Directory Indexing](#directory-indexing)
- [ ] [Directory Creation](#directory-creation)
- [ ] [Directory Management Documentation](#directory-management-documentation)

### Config Read-In

- [ ] The config file should be formatted as a .csv file. The 0th column is what the next columns are on a that row. That is to say, the 0th column on the 0th row should be `relative_path_home_directory` with the following column on the same row (i.e. the next value after the comma) being the specified relative path to the home directory. The default should be `./home_directory/`. For following rows, it may be `bloomerang_API`, `facebook_login`, etc..
- [ ] When the application first starts up, it reads in the config file.
- [ ] If the config file is unable to be found, is corrupted, or formatted incorrectly, inform the user as such and create a new config file.
- [ ] If a file of the same name already exists in that directory, the existing file's name is changed `obsolete_on_{date}.csv`.
- [ ] If a file using that `obsolete` file name already exists, simply increment an integer starting at 2 (e.g. `obsolete_on_{date}_2.csv`, `obsolete_on_{date}_3.csv`, ...).

### CSV Data Format

**NOTE:** One would think that for a lot of these all that needs to be stored is the raw numbers, and the source can be ignored. That may be true and the application could be modified as such, however, as I currently envision the program, it would need to track the source of the data to avoid reentering data in subsequent months. Maybe, each month is beholden only to itself, and the year is summed up from the months? I'll give it some thought.

- [ ] Regarding targets: Targets should be stored as annual, they always follow the format of 0th column being the month 1st column being the number.
- [ ] TODO: Have a talk with the stakeholder regarding how much data should be stored for each .csv. This might take a while.
- [ ] Any row can be modified by the user. Internally, this would be represented as adding a new row just before the last one with the 0th column of `{data}_user_mod` and a 1st column with a positive or negative number to be added to the original data.
- [ ] In general, if the data is monthly, it would be a .csv file with two columns: 0th referring to the source of the numbers and 1st referring to the number. The last row should always be: 0th column `total` and 1st column total sum. This total should ALWAYS be updated by summing the entire .csv file, and is only stored for convenience sake. It shouldn't be modified directly, and if the file ever changes, it should be re-totaled.
- [ ] In general, if the data is annual, it would be a .csv file with two columns: 0th referring to the month and 1st referring to the number.
- [ ] If the data is supposed to be cumulative, the application will simply sum-up the annual .csv file.
- [ ] Marketing Messages: 0th is source, 1st is number. Annual is standard annual. Cumulative is standard cumulative. Target is non-cumulative sum of each month (so standard annual).
- [ ] Community Events: 0th is data, 1st is event name, 2nd is Attendees. Annual is standard annual. Cumulative is standard cumulative. Target is non-cumulative sum of each month (so standard annual).
- [ ] Figure out how EXP/LEAP Nom-App-Enroll should be stored (i.e. just numbers and dates, or everything (numbers and dates seems better and easier for what this application is meant to be)). Target is cumulative sum of each month (so standard cumulative) for nominations, applications, and enrollment for both EXP and LEAP.
- [ ] Lectures: 0th is title, 1st is date, 2nd is Calvert Attendance, 3rd is Charles Attendance, 4th is St. Mary's Attendance, 5th others, 6th satisfaction. Not monthly, not standard annual, standard cumulative for each column after 1st. Target is cumulative sum of each month (so standard cumulative) for how many lectures there were, and how many attendees there were, and the percentage of satisfaction.
- [ ] Surveys: Not monthly, standard annual, standard cumulative. Target is cumulative sum of each month (so standard cumulative).
- [ ] Fundraising: Stored annually, but not standard. The 0th column is the date, the 1st is the event, 2nd is revenue source, 3rd is the raised revenue. The last row is 0th column `total` and 1st total sum of revenue. Target is cumulative sum of each month (so standard cumulative) for the revenue.
- [ ] LSMAA Membership: Standard annual and standard cumulative. Target is cumulative sum of each month (so standard cumulative) for number of members.
- [ ] LSMAA Revenue: Standard annual and standard cumulative. Target is cumulative sum of each month (so standard cumulative) for the revenue.
- [ ] Program sponsor: 0th is date, 1st program sponsor, 2nd number, 3rd level, 4th revenue. Second to last row is a sum of all the event sponsors. Last row has 0th column as `total` and 1st as total sum of revenue. Target is cumulative sum of each month (so standard cumulative) for the number of program sponsors.
- [ ] Lunch sponsor: 0th is date, 1st is lunch sponsor, 2nd is session, 3rd is pledged or paid, 4th is revenue. Second to last row is sum of all the lunch sponsors. Last is 0th column being `total` and 1st column being total sum of revenue. Target is cumulative sum of each month (so standard cumulative) for the number of lunch sponsors.
- [ ] Event sponsor: 0th is date, 1st is event sponsor, 2nd is event, 3rd is revenue. Second to last is a sum of all event sponsors, last is the sum of revenue. Target is cumulative sum of each month (so standard cumulative) for the number of event sponsors.
- [ ] Total sponsor revenue: This is just a sum of all the revenue of each sponsor. It should be 0th column as month, 1st as revenue. Target is the cumulative sum of each month (so standard cumulative) for the revenue.

### In-RAM Data Object

### In-RAM Year Object

### In-RAM Report Object

### Directory Indexing

- [x] Write a function that non-recursively looks in the directory passed as an argument for all folders that follows the format of `####-####`. It returns a list where each element is a tuple in which the first element is the name of the folder and the second element is the path to the folder.
- [x] Write a function that non-recursively looks in the directory passed as an argument for all folders that follow the format of `{mon : mon is an element of {Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec}} and {n : n is not an element of {1} and n is an element of the Natural Numbers}` `mon Report{{},_n}`. Or, in human words, has a month of the year, followed by the word " Report" followed by either nothing or an underscore with some number that isn't "0" or "1". It returns a list where each element is a tuple in which the first element is the name of the folder and the second element is the path to the folder.
- [x] Write a function that non-recursively looks in the directory passed as an argument for all folders that follow the format of `{mon : mon is an element of {Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec}} and {n : n is not an element of {1} and n is an element of the Natural Numbers}` `mon Report{{},_n} Draft{{},_n}}`. Or, in human words, has a month of the year, followed by the word " Report" followed by either nothing or an underscore with some number that isn't "0" or "1", followed by the word " Draft" followed by either nothing or an underscore with some number that isn't "0" or "1". It returns a list where each element is a tuple in which the first element is the name of the folder and the second element is the path to the folder.

### Directory Creation

- [ ] Write a function that creates a directory named `####-####` in the directory passed as an argument, where `####-####` is passed as an argument and is current fiscal year for LSM. The function should also create a .csv named `configs` and fill it with the default data per [CSV Data Format](#csv-data-format). The function should create a sub-directory named `Inputs`. Inside of `Inputs`, it should create a sub-directory named `Targets`. Inside of `Targets`, it should create a .csv for each Target and fill it with the default data per [CSV Data Format](#csv-data-format). Inside of `Inputs`, it should create a sub-directory named `Annual Goals`. Inside of `Annual Goals`, it should create a .csv for each annual goal and fill it with the default data per [CSV Data Format](#csv-data-format).
- [ ] Write a function that creates a directory named `{mon : mon is an element of {Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec}}` `mon Report` in the directory passed as an argument. If a directory of that same name already exists, the function should append a `{_n : n is not an element of {1} and n is an element of the Natural Numbers}` to the end of the directory's name. It should incrementally check each possible name until it finds one that fits. The function should then create two sub-directories, one named `Data` and the second named `Outputs`. Inside of `Data`, the function should create a .csv for each of the monthly goals and fill them with the default data per [CSV Data Format](#csv-data-format).

### Directory Management Documentation

- [ ] Comment each function in the `directory_management.py` file, and add a comment to the top of the file explaining what happens in this file.
- [ ] Write external documentation, ...

## Year Management

**Definition of Done:** The application can create and edit years, including targets, annual data, and specifying the comparison year.

**Time:** This should take a few hours.

**As a stakeholder,** **I want** to be able to create years, edit the targets, and add and modify annual data, **so that** I can set up the years for each report, modify anything if new information comes in, and ensure that each report is accurate.

### Year Management - Tasks

## Report Management

**Definition of Done:** The application can create reports, save report drafts, and onload new reports, re-generated reports, and report drafts.

**Time:** This could take a day.

**As a stakeholder,** **I want** to be able to create and recreate reports and save a draft of a report, **so that** at a click of a button, the application can onload the information available and allow editing of reports.

### Report Management - Tasks

## Data Visualization

**Definition of Done:** The application can render graphs, display targets, and display data, both annual and monthly. It can display the data for each sub-goal, as well the overall goal performance summary.

**Time:** This could take a day.

**As a stakeholder,** **I want** the ability to see the data that has been rendered prior to the report being finalized, **so that** I can determine if the data has been correctly inputted and that there are no glitches.

### Data Visualization - Tasks

## Data Modification

**Definition of Done:** The application can accept user input to change each aspect of each data. The application can add new data sources as user defined. The application can modify even the goal performance summary.

**Time:** This could take a few hours.

**As a stakeholder,** **I want** the ability to modify the data prior to the report being finalized, **so that** I can fix any mistakes I found in the data and ensure that the report looks as accurate as it would if I had created it manually.

### Data Modification - Tasks

## Report Finalization

**Definition of Done:** The application can save all the data used in the report into the report's inputs folder, internalizing any modifications made by the user.

**Time:** This could take a few hours.

**As a stakeholder,** **I want** the program to be able to save the report and the data used therein, **so that** I can revisit the exact data used to create the report in the future.

### Report Finalization - Tasks

## Render Data

**Definition of Done:** The application, using in-RAM information, can produce a PDF KPI Dashboard report of comparable quality and with the same information that could be generated by hand.

**Time:** This user story shouldn't take much longer than a day.

**As a stakeholder,** **I want** a PDF KPI Dashboard report, **so that** I don't have to manually place the information into a Word document.

### Render Data - Tasks

- [ ] [Research HTML to PDF](#research-html-to-pdf)
- [x] [Research Python into HTML](#research-python-into-html)
- [ ] [Research Plots into HTML](#research-plots-into-html)
- [ ] [Code Python into HTML](#code-python-into-html)
- [ ] [Code HTML and CSS](#code-html-and-css)
- [ ] [Code HTML to PDF](#code-html-to-pdf)

### Research HTML to PDF

- [ ] [WeasyPrint](https://weasyprint.org/)
- [ ] [Installation](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#windows)
- [x] Determine if WeasyPrint can do what I want it to do.

**Conclusion:** WeasyPrint certainly can. Although, installation may be a slight bother.

### Research Python into HTML

- [x] Python HTML Parsers.
- [x] [HTMLParser](https://docs.python.org/3/library/html.parser.html).
- [x] [Py-HTML](https://mansoorbarri.com/guides/py-html-editor/).
- [x] [Reddit](https://www.reddit.com/r/learnpython/comments/b1oq9n/python_to_changereplace_text_in_html_file/).
- [x] [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) (probably has too much for me (but definition has what I need)).
- [x] [Jinja](https://jinja.palletsprojects.com/en/stable/).

**Conclusion:** There's plenty of options, it can certainly be done. I'll probably use Jinja.

### Research Plots into HTML

- [ ] [TKinter](https://www.scaler.com/topics/matplotlib/tkinter-matplotlib/).
- [ ] [CustomTKinter](https://medium.com/@lukasschaub/modern-graphical-user-interfaces-using-python-customtkinter-80f42b698eaf).
- [ ] [HTMLWriter/MPLD3/Plotly](https://www.scivision.dev/python-html-plotting-iframe-share/).
- [ ] [Plotly](https://plotly.com/python/) for plots and [Plotly](https://plotly.com/python/interactive-html-export/) for into HTML.

**Conclusion:** At the bare minimum, I can get the plot as a .png, then save that into the HTML/PDF. ~~For the GUI, the two sub-tasks seem to work.~~ (?) It's funny, looking into Plotly, the opposite seems to be the case. I can easily render the plot into HTML, but I cannot so easily render it in TKinter. It might make sense to save the .png and load that into TKinter. I might (I won't) use MatPlotLib to render the graph for TKinter and Plotly for HTML (the graphs would look different, however slightly, and it wouldn't be worth it.)

### Code Python into HTML

- [ ] TODO.

### Code HTML and CSS

- [ ] TODO.

### Code HTML to PDF

- [ ] TODO.

## GUI

**Definition of Done:** The framework and functionality that will be used for the GUI is well-researched and experimented with. The files are set up so that each page can simply be placed in with remarkable ease.

**Time:** This shouldn't take longer than a day.

**As a developer,** **I want** the GUI platform and framework to be well-researched, **so that** I don't make mistakes while building the GUI that could cause significant time-loss.

### GUI - Tasks

- [ ] [Research PyUIBuilder](#research-pyuibuilder)

### Research PyUIBuilder

- [ ] [PyUIBuilder](https://pyuibuilder.com/).
- [ ] [GitHub](https://github.com/PaulleDemon/PyUIBuilder).
- [x] Look into the licensing.

**Conclusion:** Looks like I'm free to use so long as I only use the WebApp.

## Homepage

**Definition of Done:** The homepage should launch when the user opens the application. It should show a list of the years that the application was able to index. In one corner, it should display a settings button and a button to see the report drafts.

**Time:** This shouldn't take longer than a couple of hours.

**As a stakeholder,** **I want** a homepage, **so that** when I open the application, I can see a visual list of the years that the application has found, I can access them, and I can start using the application.

### Homepage - Tasks

## Settings Page

**Definition of Done:** A settings page exists and can be accessed by a button on any page. This settings page displays the ability to set a home directory for the application, modify credentials and API keys, and affect certain visual aspects of the application.

**Time:** This could take a while. Most likely not longer than a day. But depending on how ambitious the application gets, perhaps longer.

**As a stakeholder,** **I want** a settings page, **so that** I can change where the files get generated, update credentials and API keys for data sources, and certain, visual aspects of the application.

### Settings Page - Tasks

## Report Draft Page

**Definition of Done:** A page filled with all report drafts that can be accessed via the homepage. Each report can be clicked on, which will take the user to the report validation page for that report draft.

**Time:** This shouldn't take that long. It's just another list of buttons. I doubt much longer than an hour.

**As a stakeholder,** **I want** a page of all report drafts, **so that** I can revisit reports that I stopped in the middle of and can finish them without losing progress.

### Report Draft Page - Tasks

## New Year Page

**Definition of Done:** A page that can be accessed from the homepage that allows the user to create a new year. They should be able to specify which year it is. There cannot exist two of the same year. They should be able to set targets for each sub-goal. They should also be able to specify which year should be used as a comparison year. None should be an option. If the selected comparison year has any months with multiple reports, zero reports, or conflicting data between the year and the month, the user will be prompted to resolve conflicts. The resolution can be skipped. In that case, for the conflict months, the comparison simply will not exist. The resolution may require the user to make a new report for that month in that year. The application will explain if so.

**Time:** No longer than a day. Hopefully much less.

**As a stakeholder,** **I want** a page that can create a new year, **so that** I can use the application in multiple years, with multiple reports, and have them access previous years' data for comparison purposes.

### New Year Page - Tasks

## Year Page

**Definition of Done:** A page that can be accessed by clicking on the specific year's button on the home page. In one corner, an edit year button will exist that, if clicked, will take the user to the edit year page for that year. In the center of the screen, a list of all months that the application was able to index for that year. At the top of the list, a new report button will exist. Clicking on the new report button will take the user to the new report page. Clicking on any of the reports will take the user to the report validation page for that report.

**Time:** This is, once again, just a list of buttons. Hopefully, it shouldn't take much time.

**As a stakeholder,** **I want** a page that allows me to edit a year and displays all the reports for the selected year, **so that** I can edit annual data and targets and create new reports, edit old reports, and view all the reports that have been created in that year.

### Year Page - Tasks

## Edit Year Page

**Definition of Done:** A page that can be accessed by clicking the edit year button on a year's page. This page will display two buttons: one for editing the year's annual data and one for editing the year's targets. Each button should take the user to a new page. Clicking on the annual data button will take the user to a page that displays all the annual data in distinct boxes that can be edited. Any edits to the annual data will ask the user where this new data comes from. The user can refuse to answer, specify a new source, or edit the data of an existing source. Clicking on the target button will take the user to a grid of distinct boxes with one sub-goal's targets in each box. Clicking a box will allow the user to edit it.

**Time:** This one could take a while. It requires passing data from the front end to the back end. Maybe a day, possibly two.

**As a stakeholder,** **I want** to be able to edit years, **so that** I can update targets if new information has come in and update annual data for each new month.

### Edit Year Page - Tasks

## New Report Page

**Definition of Done:** A page that can be accessed by clicking on the new report button on a year page. This page will ask the user for which month the report should be generated. It will autofill the previous month, but the user can override that. If the user attempts to generate a report for a month that already has a report, the application will explain to the user that they will be creating a report for a month that already has one, and ask them if they want to proceed.

**Time:** This should be both easy and hard. On one hand, it is just a simple page with a month drop down list, a check, and a continue button. On the other hand, this will be the page that actually generates a new report. If the code is set up properly, so all this page needs to do is call a function, then it shouldn't take longer than an hour.

**As a stakeholder,** **I want** a page to generate a new report, **so that** I can create a KPI report for each month.

### New Report - Tasks

## Report Validation Page

**Definition of Done:** This page can be accessed in two ways: clicking continue on the new report page and clicking edit on any report on the year page. This page will display (either sequentially or in a grid (not sure yet)) each sub-goal along with the data used to get this sub-goal, it's target, the comparison year, and whether or not the graph should be included. The user can modify any aspect of the sub-goal but will be reminded that certain modifications may cause confusion as ALL modifications only apply to this report. That is to say, the user may modify the target value, but that will not update the target value in the year, which means the next report will have a different target value. The user can modify a cumulative annual sub-goal, but that new data will only be used in the next month if the data being modified was set for this month. That is to say, the user may modify the data from the previous month in this month, but then that data will not be updated. Only current data will be updated in the year and only that will get used for the next report. The user will be advised that it makes more sense for the cumulative, annual data to be modified in the year prior to making the monthly report. For each data modified, the user will be asked to list a source. They may list anything there or nothing. They may even modify the data of an already existing source. When each sub-goal is as the user wants it to be, the user will be taken to the goal performance summary screen for each goal. The user will be, once again, prompted to modify the data as they wish. Once finished, the report validation page will close and the PDF will be displayed.

**Time:** This, definitively, will take the longest. It is the meat and bones of the application. The part that causes each distinct part to interact the most. This is where the user will create the report, modify the report, add new data in, and plenty of other things. It could take several days.

**As a stakeholder,** **I want** the ability to validate each piece of data before the report is generated, **so that** I can ensure that the data is correct, input data that needs to be inputted manually, modify any data that might need modification, and ensure that the KPI Dashboard report is as accurate and correct as if I had done the whole thing manually.

### Report Validation - Tasks
