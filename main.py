import PySimpleGUI.PySimpleGUI as sg
import random as rn
import webbrowser
import logging

from modules.quotes import quotes_load
import modules.appdata as appdata


# TODO: Put this somewhere 
logger= logging.getLogger(__name__)
    
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler("main.log", mode="w")
formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s -> %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


# TODO: Create file with motivational quotes

class RBProgram:
    # TODO: Eventually move this to a separate module
    def __init__(self):
        self.goal = None
        self.streak = None
        self.start_date = None
        self.why_I_quit = ""    # Maybe move this one in some kinda dictionary, integrated with diary

    def __str__(self):
        return f"{self.goal} days goal started on {self.start_date}."

    def set_goal(self, goal):
        self.goal = goal

# TODO: Move layouts creations to layouts module
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
        goal_val = 30
        startdate_val = None
 
    layout = [[sg.Text("Duration of challange: "), sg.Spin([n for n in range(1,1000)], goal_val, key="-duration-")],
        # TODO add today date and date handling using datetime
            [sg.Text("I'm starting on "), sg.InputText("todaydate", key="-date-")],
            [sg.Text("This is why I want to quit:")],
            [sg.Multiline(RBClass.why_I_quit, key="-whyIquit-")],
            [sg.Button("OK"), sg.CloseButton("Close")]]
    return layout


if __name__ == "__main__":

    # Load program class:
    program = appdata.load()
    logger.debug(program)

    # If program class was not yet created, init new one.
    # TODO: init new class if changes were made in class too 
    if program is None:
        program = RBProgram()
        logger.info("Initialized new program instance")

    # Create window:
    quote_data = quotes_load()
    sg.theme("DarkBrown1")
    layout = create_layout(program)
    window = sg.Window("The Rebooot program", layout,  resizable=True, icon=None)  # TODO: add custom icon

    # Mainloop:
    while True:
        event, values = window.read()

        # For debugging:
        def __str__():
            return values
        logger.debug(f"{event} {values}")

        if event in (None, 'Cancel'):
            break

        #Events from goal menu:
        if event in ("Edit Goal", "New Goal"):
            if event == "Edit Goal":
                edit = True
            else: 
                edit = False

            # Create and launch goal window, blocking:
            goal_layout = create_goal_layout(program, edit)
            # Kinda buggy when new widnow is opened, try fixing it
            goal_window = sg.Window("Set Goal", goal_layout)
            while True:
                g_event, g_value = goal_window.read()
                
                logger.debug(f"Goal window: {event} {values}")

                # Throws TypeError
                try:
                    if g_event in ("Close"):
                        goal_window.Close()
                        logger.info("Goal window closed without saving")

                    if g_event in ("OK"):
                        # TODO: Save values to program class here
                        def __str__():
                            return logger.debug(g_value["-duration-"], g_value["-date-"])
                        goal_window.Close()
                        logger.info("Goal window closed (with save)")

                except TypeError as e:
                    logger.error("Expected 'TypeError'", exc_info=True)
                    break

        # Events from help menu:
        if event in ("Github Page"):
            webbrowser.open("https://github.com/LittlepawD/TheReBootProgram")

        if event in ("NoFap"):
            webbrowser.open("https://nofap.com/")
    # End:
        try:
            # TODO: Save data and log on program crash
            appdata.save(program)
        except Exception as e: 
            logger.error("Program crash")
            
