def APP_CONFIGS() -> list[list[str]]:
    return [['config', 'value'], 
            ['home_directory', '.testdata'],
            ['button_width', '40'],
            ['button_height', '40'],
            ['comp_year_color', '#CC0000'],
            ['target_color', '#008800'],
            ['year_color', '#0000CC']]
def DATA() -> list[list[str]]:
    return [['data_file_name', '(date,data_column_one,data_column_two,...)'], 
            ['marketing_messages', '(date,source,messages)'], 
            ['community_events', '(date,event_name,attendees)'],
            ['exp_nominations', '(date,nominations)'],
            ['exp_applications', '(date,applications)'], 
            ['exp_enrollment', '(date,enrollment)'],
            ['leap_nominations', '(date,nominations)'],
            ['leap_applications', '(date,applications)'],
            ['leap_enrollment', '(date,enrollment)'],
            ['lectures', '(date,title,calvert,charles,st_mary,satisfaction)'],
            ['surveys', '(date,surveys)'],
            ['fundraising', '(date,event,source,revenue)'], 
            ['lsmaa', '(date,enrollment,revenue)'], 
            ['program_sponsors', '(date,sponsor,number,level,revenue,notes)'], 
            ['lunch_sponsors', '(date,sponsor,session,pledged_paid,revenue,notes)'],
            ['event_sponsors', '(date,sponsor,event,revenue,notes)']]
def GOALS(year: int) -> list[list[str]]:
    return [['goal', 'percentage', '(sub_goal_zero,sub_goal_one,sub_goal_two,...)'],
            ['Value Proposition & Visibility', '50', f'(Marketing Messages,Community Events,EXP {year + 1} Nominations,EXP {year + 1} Applications,EXP {year + 1} Enrollment,Leap {year} Nominations,Leap {year} Applications,Leap {year} Enrollment)'], 
            ['Community Engagement', '50', "(LSM Lectures,Lecture Attendance,Calvert Attendance,Charles Attendance,St. Mary's Attendance,Satisfied-Very Satisfied,Interest Surveys)"], 
            ['Revenue', '50', '(Fundraising Event Revenue,LSMAA Membership,LSMAA Revenue,Program Sponsors,LSM Lunch Sponsors,LSM Event Sponsors,Sponsorship Revenue)']]
def SUB_GOALS(year: int) -> list[list[str]]:
    return [['sub_goal', 'data_file', 'time', 'summed_column', 'committee', 'show_graph'],
             ['Marketing Messages', 'marketing_messages', 'Monthly', 'messages', 'Communications', 'True'],
             ['Community Events', 'community_events', 'Monthly', 'rows', 'Communications', 'True'],
             [f'EXP {year + 1} Nominations', 'exp_nominations', 'Annual', 'nominations', 'Recruiting', 'True'],
             [f'EXP {year + 1} Applications', 'exp_applications', 'Annual', 'applications', 'Recruiting', 'True'],
             [f'EXP {year + 1} Enrollment', 'exp_enrollment', 'Annual', 'enrollment', 'Recruiting', 'True'],
             [f'Leap {year} Nominations', 'leap_nominations', 'Annual', 'nominations', 'Leap/Recruiting', 'True'],
             [f'Leap {year} Applications', 'leap_applications', 'Annual', 'applications', 'Leap/Recruiting', 'True'],
             [f'Leap {year} Enrollment', 'leap_enrollment', 'Annual', 'enrollment', 'Leap/Recruiting', 'True'],
             ['LSM Lectures', 'lectures', 'Annual', 'rows', 'Alumni', 'False'],
             ['Lecture Attendance', 'lectures', 'Annual', '(calvert,charles,st_mary)', 'Alumni', 'False'],
             ['Calvert Attendance', 'lectures', 'Annual', 'calvert', 'Alumni', 'False'],
             ['Charles Attendance', 'lectures', 'Annual', 'charles', 'Alumni', 'False'],
             ["St. Mary's Attendance", 'lectures', 'Annual', 'st_mary', 'Alumni', 'False'],
             ['Satisfied-Very Satisfied', 'lectures', 'Annual', 'satisfaction', 'Alumni', 'False'],
             ['Interest Surveys', 'surveys', 'Annual', 'surveys', 'alumni/program', 'False'],
             ['Fundraising Event Revenue', 'fundraising', 'Annual', 'revenue', 'Development', 'True'],
             ['LSMAA Membership', 'lsmaa', 'Annual', 'enrollment', 'Alumni', 'True'],
             ['LSMAA Revenue', 'lsmaa', 'Annual', 'revenue', 'Alumni', 'True'],
             ['Program Sponsors', 'program_sponsors', 'Annual', 'rows', 'Development', 'True'],
             ['LSM Lunch Sponsors', 'lunch_sponsors', 'Annual', 'rows', 'Program', 'True'],
             ['LSM Event Sponsors', 'event_sponsors', 'Annual', 'rows', 'Development', 'True'], 
             ['Sponsorship Revenue', '(program_sponsors,lunch_sponsors,event_sponsors)', 'Annual', 'revenue', 'Development', 'True']]
def YEAR_CONFIGS(year: str, comp_year: str) -> list[list[str]]:
    return [['config', 'value'], 
            ['year', f'{year}'],
            ['comp_year', f'{comp_year}']]
def MONTH_CONFIGS(year_directory: str, month: str) -> list[list[str]]:
    return [['config', 'value'],
            ['year_directory', f'{year_directory}'],
            ['month', f'{month}'],
            ['access_directory', f'{year_directory}'],
            ['versions', '()']]
