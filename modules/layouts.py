import PySimpleGUI as sg
from datetime import date
from modules.quotes import quotes_load


def create_main_layout(program):
    menu_def = [["&Goal", ["New Goal", "Edit Goal",]],
                 ["&Diary", ["Open", "Export",]],
                 ["&Options"],
                 ["Help", ["Github Page", "NoFap"]]]
    options_bar = [sg.Menu(menu_def)]
    # TODO: Fix menu bar not displaying on MacOS

    streak_bar_font = ("Helvetica", 20)
    streak_bar = [sg.Text(f"Streak:", font=streak_bar_font),
                sg.Text(program.streak, font=streak_bar_font, key="-streak-"),
                sg.VerticalSeparator(),
                sg.Text(f"Goal:", font=streak_bar_font),
                sg.Text(program.goal, font=streak_bar_font, key="-goal-")]

    quote_data = quotes_load()
    quote = [sg.Text(quote_data)]

    col_calendar = [[sg.Text("Calendar placeholder")]]
    col_buttons = [[sg.Button("Calendar f1")],
                    [sg.Button("Calendar f2")],
                    [sg.Button("Calendar f3")]]
    calendar_bar = [sg.Frame("Calendar", col_calendar, size=(350, 260)), 
                    sg.Column(col_buttons, element_justification="center",)]

    layout = [
        options_bar,
        streak_bar,
        quote,
        calendar_bar]

    return layout

def create_calendar_section(program):
    day_bar = [sg.T("Mon"), sg.("Tue"), sg.T("Wen"), sg.T("Thu"), sg.T("Fri"), sg.T("Sat"), sg.T("Sun")]

    # TODO create clickable box - objet representing day
    # to have calendar with goal starting at correct weekday, insert empty boxes in the first row.
    no_insert_columns = program.start_date.weekday()
    first_row = []
    # skip first row and start creating the second
    for day in range(7 - no_insert_columns, program.goal, 1):
        []

def create_goal_layout (program, edit):
    # To put to respective elements
    if edit:
        goal_val = program.goal
        startdate_val = program.start_date.isoformat()
        why_I_q = program.why_I_quit
    else:
        goal_val = 30
        startdate_val = date.today().isoformat()
        why_I_q = ""

    layout = [[sg.Text("Duration of challange: "), sg.Spin([n for n in range(1,1000)], goal_val, key="-duration-")],
            [sg.Text("I'm starting on "), sg.InputText(startdate_val, key="-date-")],
            [sg.Text("This is why I want to quit:")],
            [sg.Multiline(why_I_q, key="-whyIquit-")],
            [sg.Button("OK"), sg.CloseButton("Close")]]

    return layout

