import PySimpleGUI.PySimpleGUI as sg
import random as rn
import webbrowser
import logging

import modules.layouts as layouts
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
    sg.theme("DarkBrown1")
    layout = layouts.create_main_layout(program)
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
            goal_layout = layouts.create_goal_layout(program, edit)
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
            
