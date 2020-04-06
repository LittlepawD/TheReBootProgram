import PySimpleGUI.PySimpleGUI as sg
import random as rn
import webbrowser
from modules.quotes import quotes_load


# TODO: Create file with motivational quotes

class RBProgram:
    # TODO: Eventually move this to a separate module
    def __init__(self, DATA):
        # TODO: get saved data from DATA and assign to variables
        self.goal = None
        self.streak = None

    def set_goal(self, goal):
        self.goal = goal


def create_layout(RBClass):
    menu_def = [["&Goal", ["Reset", "Edit",]],
                 ["&Diary", ["Open", "Export",]],
                 ["&Options"],
                 ["Help", ["Github Page", "NoFap"]]]
    options_bar = [sg.Menu(menu_def)]

    streak_bar_font = ("Helvetica", 20)
    streak_bar = [sg.Text(f"Streak: {RBClass.streak}", font=streak_bar_font),
                sg.VerticalSeparator(),
                sg.Text(f"Goal: {RBClass.goal}", font=streak_bar_font)]

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


if __name__ == "__main__":

    # Init RBClass:
    SAVED_DATA = None  # TODO Prepare saved data file (format - .py module?)
    Program = RBProgram(SAVED_DATA)
    # Create window:
    quote_data = quotes_load()
    sg.theme("DarkBrown1")
    layout = create_layout(Program)
    window = sg.Window("The Rebooot Program", layout,  resizable=True, icon=None)  # TODO: add custom icon

    # Mainloop:
    while True:
        event, values = window.read()

        # For debugging:
        print(event)
        print(values, "\n")

        if event in (None, 'Cancel'):
            break

        # Events from help menu:
        if event in ("Github Page"):
            webbrowser.open("https://github.com/LittlepawD/TheReBootProgram")

        if event in ("NoFap"):
            webbrowser.open("https://nofap.com/")
    # End:
    window.close()
