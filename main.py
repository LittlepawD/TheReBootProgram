import PySimpleGUI.PySimpleGUI as sg
import random as rn
import webbrowser

from modules.quotes import quotes_load
import modules.appdata as appdata


# TODO: Create file with motivational quotes

class RBProgram:
    # TODO: Eventually move this to a separate module
    def __init__(self):
        self.goal = None
        self.streak = None
        self.start_date = None

    def __str__(self):
        return f"{self.goal} days goal started on {self.start_date}."

    def set_goal(self, goal):
        self.goal = goal


def create_layout(RBClass):
    menu_def = [["&Goal", ["New Goal", "Edit Goal",]],
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

def create_goal_layout (RBClass, edit):
    # To put to respective elements
    if edit:
        goal_val = RBClass.goal
        startdate_val = RBClass.start_date
    else:
        goal_val = None
        startdate_val = None
 
    layout = [[sg.Text("Goal")]]
            # [sg.Button("OK")], [sg.CloseButton("Close")]]


if __name__ == "__main__":

    # Load program class:
    program = appdata.load()
    print(program)
    # If program class was not yet created, init new one.
    if program is None:
        print("Initializing new program instance...")
        program = RBProgram()


    # Create window:
    quote_data = quotes_load()
    sg.theme("DarkBrown1")
    layout = create_layout(program)
    window = sg.Window("The Rebooot program", layout,  resizable=True, icon=None)  # TODO: add custom icon

    # Mainloop:
    while True:
        event, values = window.read()

        # For debugging:
        print(event)
        print(values, "\n")

        if event in (None, 'Cancel'):
            break

        #Events from goal menu:
        if event in ("Edit Goal", "New Goal"):
            if event == "Edit Goal":
                edit = True
            else: 
                edit = False

            # Create and launch goal window, blocking:
            # Work in progress, Throws ValueError
            # goal_layout = create_goal_layout(program, edit)
            # goal_window = sg.Window("Set Goal", goal_layout)
            # while True:
            #     g_event, g_value = goal_window.Read(timeout=1000)
            #     if g_event in (None, "Close"):
            #         break
                
            #     if g_event in ("OK"):
            #         # TODO: Save values to program class here
            #         print("ok")
            #         break

        # Events from help menu:
        if event in ("Github Page"):
            webbrowser.open("https://github.com/LittlepawD/TheReBootProgram")

        if event in ("NoFap"):
            webbrowser.open("https://nofap.com/")
    # End:
    appdata.save(program)
    window.close()

    # TODO: Save data and log on program crash
