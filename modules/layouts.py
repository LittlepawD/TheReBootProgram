import PySimpleGUI as sg
from modules.quotes import quotes_load

def create_main_layout(program):
    menu_def = [["&Goal", ["New Goal", "Edit Goal",]],
                 ["&Diary", ["Open", "Export",]],
                 ["&Options"],
                 ["Help", ["Github Page", "NoFap"]]]
    options_bar = [sg.Menu(menu_def)]

    streak_bar_font = ("Helvetica", 20)
    streak_bar = [sg.Text(f"Streak: {program.streak}", font=streak_bar_font),
                sg.VerticalSeparator(),
                sg.Text(f"Goal: {program.goal}", font=streak_bar_font)]

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


def create_goal_layout (program, edit):
    # To put to respective elements
    if edit:
        goal_val = program.goal
        startdate_val = program.start_date
    else:
        goal_val = 30
        startdate_val = None
 
    layout = [[sg.Text("Duration of challange: "), sg.Spin([n for n in range(1,1000)], goal_val, key="-duration-")],
        # TODO add today date and date handling using datetime
            [sg.Text("I'm starting on "), sg.InputText("todaydate", key="-date-")],
            [sg.Text("This is why I want to quit:")],
            [sg.Multiline(program.why_I_quit, key="-whyIquit-")],
            [sg.Button("OK"), sg.CloseButton("Close")]]
    return layout

