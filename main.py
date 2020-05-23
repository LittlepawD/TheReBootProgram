import PySimpleGUI.PySimpleGUI as sg
import random as rn
import webbrowser
import logging
from datetime import date

# dev:
import time

import modules.layouts as layouts
import modules.appdata as appdata
import modules.journal as journal


# TODO: Create file with motivational quotes

class RBProgram:
    """ Class representing the reboot program.

    Attributes:
        self.has_goal {bool} -- helps track if goal was already set.
        self.goal {int} -- length of the goal in days.
        self.startdate {datetime.date} -- Day when goal was started as datetime date object.
        self.streak {int} -- number of days elapsed from startdate.
        self.why_I_quit {str}

    Methods:

    """

    # TODO: Eventually move this to a separate module
    def __init__(self):
        self.has_goal = False
        self.goal = None
        self.streak = None
        self.start_date = None
        self.why_I_quit = ""  # Maybe move this one in some kinda dictionary, integrated with diary

    def __str__(self):
        return f"{self.goal} days goal started on {self.start_date}."

    def set_goal(self, goal, startdate=None, why_I_quit=""):
        """ Set program atributes from parameters.
        Arguments:
            goal {int} -- length of the goal in days.
            startdate {str} -- String representing startdate in isoformat (YYYY-MM-DD). If None, today date is set. (default: {None})
            why_I_quit {str} -- (default: {""})
        """
        self.goal = goal
        self.has_goal = True
        if not startdate:
            self.start_date = date.today()
        else:
            self.start_date = date.fromisoformat(startdate)
        self.why_I_quit = why_I_quit
        logger.info(f"set_goal: New goal set - {self}")

    def update_streak(self):
        self.streak = (date.today() - self.start_date).days
        logger.debug(f"Streak updated -- {self.streak}")

    def update_days_colors(self, window):
        """ Updates day colors in calendar - successful days green, today orange. """
        for day in range(self.streak):
            window[f"-D:{day}-"].update(button_color=("white", "green"))
        window[f"-D:{self.streak}-"].update(button_color=("white", "orange"))
        window[f"-D:{self.streak}-"].SetFocus()

def mainloop():
    # Create window:
    sg.theme("DarkBrown1")
    # debuging:
    timer = time.time()
    diary = journal
    filename = None
    layout = layouts.create_main_layout(program)
    window = sg.Window("The Rebooot program", layout, resizable=True, icon=None)  # TODO: add custom icon
    window.finalize()
    if program.has_goal:
        program.update_days_colors(window)
    logger.debug(f"Main window created in {time.time() - timer} s.")
    # Mainloop:
    while True:
        event, values = window.read()

        # For debugging:
        def __str__():
            return values

        logger.debug(f"Main window: {event} {values}")

        if event in (None, 'Cancel'):
            break

        # Events from goal menu:
        if event in ("Edit Goal", "New Goal"):
            if event == "Edit Goal" and program.goal:
                edit = True
            else:
                edit = False

            # Create and launch goal window, blocking:
            goal_layout = layouts.create_goal_layout(program, edit)
            # Kinda buggy when new widnow is opened, try fixing it
            goal_window = sg.Window("Set Goal", goal_layout)
            while goal_window:
                g_event, g_values = goal_window.read()
                logger.debug(f"Goal window: {event} {values}")

                try:
                    if g_event in ("Close"):
                        goal_window.Close()
                        del goal_window
                        break

                        logger.debug("Goal window closed properly without saving")

                    if g_event in ("OK"):
                        def __str__():
                            return logger.debug(g_values["-duration-"], g_values["-date-"])

                        # Save new values to program class:
                        # TODO: Check that date was entered in proper format
                        program.set_goal(g_values["-duration-"], g_values["-date-"], g_values["-whyIquit-"].strip())

                        # Update Main window so changes take effect:
                        window["-goal-"].update(program.goal)
                        program.update_streak()
                        window["-streak-"].update(program.streak)

                        # TODO update callendar section after editing goal!!!
                        # window["-calendar-frame-"].update(layout=layouts.create_calendar(program))
                        # Doesn't work, if no other solution is found the main window will need to be restarted after goal change.
                        window["-calendar-frame-"].update("Restart program to update calendar")
                        # Doesn't work without calendar section update
                        # program.update_days_colors(window)

                        # Close goal window
                        goal_window.Close()
                        del goal_window
                        logger.debug("Goal window closed properly with save.")
                        break

                except TypeError as e:
                    logger.error("Expected 'TypeError'", exc_info=True)
                    goal_window.close()
                    del goal_window
                    logger.error("Goal window closed with error.")
                    break

        if event in ("Open"):
            journal_layout = layouts.create_journal_layout()
            # Kinda buggy when new widnow is opened, try fixing it
            journal_window = sg.Window("Journal", journal_layout, size=(600, 500), resizable=True)

            while journal_window:
                j_event, j_values = journal_window.read()
                logger.debug(f"Journal window: {event} {values}")

                if j_event in (None, 'Exit'):
                    journal_window.Close()
                    del journal_window
                    break

                if j_event in ('New............(CTRL+N)', 'n:78'):
                    filename = journal.new_file(journal_window)

                if j_event in ('Open..........(CTRL+O)', 'o:79'):
                    filename = journal.open_file(journal_window)

                if j_event in ('Save............(CTRL+S)', 's:83'):
                    journal.save_file(journal_window, j_values, filename)

                if j_event in ('Save As'):
                    journal.save_file_as(journal_window, j_values)

        # Events from help menu:
        if event in ("Github Page"):
            webbrowser.open("https://github.com/LittlepawD/TheReBootProgram")

        if event in ("NoFap"):
            webbrowser.open("https://nofap.com/")


if __name__ == "__main__":

    # Init logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler("main.log", mode="w")
    formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s -> %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Load program class:
    program = appdata.load()
    logger.debug(program)

    # If program class was not yet created, init new one.
    # TODO: init new class and migrate data if changes were made in the code
    if program is None:
        program = RBProgram()
        logger.info("Initialized new program instance")
    else:
        # If there is existing program, update streak
        program.update_streak()

    mainloop()

    # End:
    try:
        if program.goal:
            appdata.save(program)
    except Exception as e:
        logger.error("Program crash")
