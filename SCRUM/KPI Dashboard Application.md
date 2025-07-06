# KPI Dashboard Application

## Overview

## Input

The application will have a variety of data-streams programmed in. These will come from APIs and credentials stored in an external, modifiable text document.

When it loads information into the in-RAM data structures, it will do so from `.csv` files located in the folder specific for each report. When it loads information in via an API, it will automatically load store that information in a `.csv`.

That is to say, an entire report should be capable of being generated exclusively via `.csv` files.

Each year will have a folder. Each year will have one-sub folder named `inputs`. This folder will contain the information relevant to every report, that is to say, annual information. This folder will also contain a folder named `targets` that stores the targets for each sub-goal.

Each month in that year will have a folder. Each month will contain two folders: `inputs` and `outputs`. The outputs folder will store the generated PDFs for that month. The inputs folder will contain all the relevant information for just that month.

When a new report is generated in that same month, the modification made to the information will get stored in a new `.csv` (`{data}_2.csv`), and the output PDF will likewise have its name changed to `{report}_2.csv`. If any data is not changed from a previous report, a new file will not be generated.

This means that `{report}_2.csv` will look for `{data}_2.csv` unless there isn't one, then it will look for `{data}.csv`.

When a report is generated, the information taken from the year used to generate it will get stored within the month's folder. The name will follow `{data}.csv`. If a new report in that same month is being generated, it will use that old data before looking for that data from the year folder. A check box can be selected to allow looking for yearly data instead.

## Calculation

The calculation can be done with Matplotlib, Pandas, SciPy, and the like. This step doesn't do a lot. It will primarily come into play as the mid-point displayer. That is to say, it will display the data to they user, prompting whether or not the data is accurate. Any changes made to the data will get passed back from the calculation step into the input step, before returning to recalculate the data.

## Output

The output should be rendered as a PDF. The specifics as to how this can be done are up to debate and subject to change.

The current, desired method is to use the package [weasyprint](https://weasyprint.org/) which can combine CSS and HTML into a PDF. This would allow the specifics of the visual to be easily changed and modified. If the HTML file was not packaged up into the binary, then anyone with HTML or CSS skills could change the way the output PDF file looks.

I suspect, perhaps naively, that this will be one of the easiest aspects of the application.

## Main File

This is the file that starts everything up. Basically just a standard Main file. It will also contain the in-RAM data structures that Input file will load data into, the Calculation file will use to perform the proper calculations on, and the Output file will use to render the PDF.

## GUI

There are a variety of options, and it certainly requires a more in-depth look. However, [PyUIBuilder](https://pyuibuilder.com/) looks exceedingly interesting. While I was initially adverse to the idea of a drag 'n drop builder, I realized that this is a drag 'n drop *builder* that exports code to be plugged into a project.

This is very promising, as it can save time on design, and save time on implementation. It really seems like the best of both worlds.

### Home

When the application is opened, the user would be displayed with a list of the years that the application was able to index, and under each year, would be a list of all the reports that the application was able to index.

The user could click on each report, allowing the report to be [re-generated](#generate-a-report) as if it is a new report.

Alternatively, the user could click on an add report button under each year, which would [generate](#generate-a-report) a new report.

Or the user could click on an add year button, which would [generate a new year](#generate-a-year).

Or the user could click on an [edit a year](#edit-a-year) button, which would allow the user to edit the details of a year.

### Edit Targets

Here, the user would be given a list of the years the application was able to index. Under each year, the user would be given a grid-display of each sub-goal. Clicking on a sub-goal would display the targets for that sub-goal for each month.

### Generate a Report

~~When the user is either generating a new report or re-generating an old report, they are taken to the generate a report page.~~

~~In either case, the application will ask which month and year the user wants to generate the report for. If the user clicked a re-generate a report option, it will autofill the year and month of the report the user selected to re-generate. If the user clicked a generate a report option, it will autofill the previous month based off the user's system clock, and use the year that the user selected the generate a report under.~~

~~If the user specifies a year that isn't indexed, the application will prompt the user to make sure that they want to start a new year. If the user specifies a month that isn't indexed in a year that is, the application will prompt the user to make sure that they want to generate a report for a new month, instead of an old month.~~

~~If the user presses on to generate a new year, they will be taken to the [generate a year](#generate-a-year) page.~~

~~If the user presses on to generate a new month, the application will begin to onload the data from all the datasources specified in [Input](#input). The application will then move onto [report validation](#report-validation).~~

~~If the user presses on to re-generate a pre-existing month, the application will ask if the user would like to use the data from the month's folder or the year's folder, but only if the data doesn't match, and then move on to [report validation](#report-validation).~~

None of that make much sense. When the user clicks to edit a report, they'll just be taken straight to the report validation page.

When a user wants to create a new report, then they'll be asked which month they want. They would only be able to create a new report under a year, so it doesn't need to ask for the year.

### Report Validation

The report validation page will display the in-RAM information as on-loaded by the the [Input](#input) section.

Each sub-goal will be displayed in a page (one at a time or in a grid), along with an accept or edit option for each.

The accept option will move onto the next sub-goal, and when all sub-goals have been accepted, it will move onto [Output](#output).

The edit option will allow the user to modify any aspect of the data. Specifically, they can add a new datasource (specify where the new numbers came from and how much they are), or do a general edit (the location of the new data would be specified as `user_input`), or edit each datasource's data (internally, this would be represented as a new column with the datasource being `{old_data_source}_user_offset`).

The user could also edit the any of the target values for that sub-goal (the user would be reminded that these edits are monthly specific, and if they want to edit the yearly target values, they have to go the [edit a year](#edit-a-year) page).

The final part of the report validation would be the goal performance summary. Displaying what the algorithm decided the values should be, and allowing any final added weights to be added to each goal's performance summary.

### Generate a Year

The generate a new year page will prompt the user to specify which year from the list of indexed years should be used as the previous year for data comparison. There should never not be a previous year, but if there ever is, this option will simply display "No Previous Year."

If there are any conflicts with data (i.e. one month having two reports), the application will prompt the user to specify which report and data should be used.

Next, the user will have the ability to edit the targets for each sub-goal.

~~If the user was sent to this page from a generate a report click, then they will be sent back to that page. Elsewise,~~ they will be returned to the homepage.

### Edit a Year

On the edit a year page, the user can have the opportunity to change which year and which reports should be used as the previous year for data comparison.

The user will have the opportunity to edit the target values for each sub-goal.

~~The user will be told that any already generated reports will have the data used to generate them stored in their folder.~~

## Binary

Read through [this](https://docs.python.org/3/faq/programming.html#faq-create-standalone-binary) website.

The best option appears to by PyInstaller, which would require me to build the project on a Mac device before being able to send that binary over. Same for Windows and Linux.

It's worth nothing that, from what I've seen, this is not the best use-case of Python. However, as this application is extremely simple (in the grand scheme of things), I don't think it will matter much. Nonetheless, it is important to note that I am aware that Python, in general, probably shouldn't be used to make desktop applications, and things like Electron or React would be much better.
