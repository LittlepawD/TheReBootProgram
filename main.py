import PySimpleGUI.PySimpleGUI as sg
import random as rn

# TODO: Create file with motivational quotes
QUOTES = ("You can do it!", "Success is the sum of small efforts, repeated day after day.")


class RBProgram:
    # TODO: Eventually move this to a separate module
    def __init__(self, DATA):
        # TODO: get saved data from DATA and assign to variables
        self.goal = None
        self.streak = None

    def set_goal(self, goal):
        self.goal = goal


def create_layout(RBClass):
    # TODO: Order the optionbar to topleft corner, order buttons next to each other
    options_bar = [sg.Button("set streak"), sg.Button("diary"), sg.Button("options")]
    streak_bar = [sg.Text(f"Streak: {RBClass.streak}"), sg.Text(f"Goal: {RBClass.goal}")]
    quote = [sg.Text(rn.choice(QUOTES))]

    layout = [
        options_bar,
        streak_bar,
        quote,
        [sg.Text('placeholder')]
    ]

    return layout

if __name__ == "__main__":

    # Init RBClass:
    SAVED_DATA = None   # TODO Prepare saved data file (format - .py module?)
    Program = RBProgram(SAVED_DATA)
    # Create window:
    layout = create_layout(Program)
    window = sg.Window("The Rebooot Program", layout, icon=None)  # TODO: add custom icon

    # Mainloop:
    while True:
        event, values = window.read()
        if event in (None, 'Cancel'):
            break

    # End:
    window.close()
