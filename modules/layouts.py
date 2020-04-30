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

    calendar_content = create_calendar(program)
    col_buttons = [[sg.Button("Calendar f1", focus=True)],
                    [sg.Button("Calendar f2")],
                    [sg.Button("Calendar f3")]]
    calendar_row = [sg.Frame("", calendar_content, size=(350, 260)), 
                    sg.Column(col_buttons, element_justification="center",)]

    layout = [
        options_bar,
        streak_bar,
        quote,
        calendar_row]

    return layout

def calendar_box(text="", bt_color=None, enabled=True):
    """Creates button - single calendar box in format for constructing calendar.

    Keyword Arguments:
        text {str} -- box text (default: {""})
        bt_color {("text_color", "box_color")} -- tuple specifying box colors (default: {None})
        enabled {bool} -- box is clickable -> has key and makes events (default: {True})

    Returns:
        {PySimpleGUI.Button}
    """
    if enabled and text != "":
        key = f"-D:{text}-"
    else: key=None
    # size is in no of characters, which kinda sucks
    return sg.Btn(text, key=key, size=(3,1), button_color=bt_color, font="courier 13", pad=(0,0), disabled= not enabled)

def create_calendar(program):
    days = ["Mon", "Tue", "Wen", "Thu", "Fri", "Sat", "Sun"]
    # TODO: find better colors for day boxes, these have too low contrast
    day_bar = [calendar_box(day, enabled=False, bt_color=("white","black")) for day in days]

    # to have calendar with goal starting at correct weekday, insert empty boxes in the first row.
    no_insert_columns = program.start_date.weekday()
    # more or less for testing, this should happen in constructor loop:
    first_row = [calendar_box(enabled=False, bt_color=("gray","gray")) for n in range(no_insert_columns)] \
                + [calendar_box(str(n)) for n in range(7-no_insert_columns)]
    calendar = [day_bar, first_row]

    return calendar

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
