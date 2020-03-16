import PySimpleGUI.PySimpleGUI as sg

layout = None



if __name__ == "__main__":

    # Create window:
    window = sg.Window("The Rebooot Program", layout, icon=None)  # TODO: add custom icon

    # Mainloop:
    while True:
        event, values = window.read()
        if event in (None, 'Cancel'):
            break

    # End:
    window.close()
