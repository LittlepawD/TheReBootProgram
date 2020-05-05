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

    if program.has_goal:
        calendar_content = create_calendar(program)
    else:
        calendar_content = [[sg.T("Goal not yet created!")]]

    col_buttons = [[sg.Button("Calendar f1")],
                    [sg.Button("Calendar f2")],
                    [sg.Button("Calendar f3")]]
    calendar_row = [sg.Frame("", calendar_content, size=(350, 260), key="-calendar-frame-"), 
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
	# CHECK boxes are too wide in linux desktop, change size respectively
    return sg.Btn(text, key=key, size=(3,1), button_color=bt_color, font="courier 13", pad=(0,0), disabled= not enabled)

def create_calendar(program):
    """Returns calendar to put into calendar frame
    Arguments:
        program {[RBProgram object]} - current program goal
    Returns:
        [2d-list] - rows with buttons representing days in calendar
    """    
    days = ["Mon", "Tue", "Wen", "Thu", "Fri", "Sat", "Sun"]
    # TODO: find better colors for day boxes, these have too low contrast
    day_bar = [calendar_box(day, enabled=False, bt_color=("white","black")) for day in days]
    # to have calendar with goal starting at correct weekday, insert empty boxes in the first row:
    no_insert_columns = program.start_date.weekday()

    # first row of calendar:
    calendar = [day_bar, [calendar_box(enabled=False, bt_color=("gray","gray")) for n in range(no_insert_columns)] \
                + [calendar_box(str(day)) for day in range(7-no_insert_columns)]]
    days_created = 7 - no_insert_columns

    # calendar body:
    for day in range(7 - no_insert_columns, program.goal - 7, 7):
        row = [calendar_box(str(n)) for n in range(day, day + 7)]
        calendar.append(row)
        days_created += 7
    # TODO Fix bug where 8 days appear in last row if second row starts with first day.
    last_row = [calendar_box(str(day)) for day in range(days_created, program.goal + 1)]
    last_row += [calendar_box(enabled=False, bt_color=("gray","gray")) for n in range(len(last_row),7)]
    calendar.append(last_row)
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
            [sg.Text("I'm starting on (day zero):"), sg.InputText(startdate_val, key="-date-")],
            [sg.Text("This is why I want to quit:")],
            [sg.Multiline(why_I_q, key="-whyIquit-")],
            [sg.Button("OK"), sg.CloseButton("Close")]]

    return layout
