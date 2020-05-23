import PySimpleGUI as sg

def new_file(window) -> str:

    window['_BODY_'].update(value='')
    window['_INFO_'].update(value='> New Entry <')
    filename = None
    return filename


def open_file(window) -> str:

    try:
        filename: str = sg.popup_get_file('Open File', no_window=True)
    except:
        return
    if filename not in (None, '') and not isinstance(filename, tuple):
        with open(filename, 'r') as f:
            window['_BODY_'].update(value=f.read())
        window['_INFO_'].update(value=filename)
    return filename

def save_file(window, vals, filename: str):

    if filename not in (None, ''):
        with open(filename,'w') as f:
            f.write(vals.get('_BODY_'))
        window['_INFO_'].update(value=filename)
    else:
        save_file_as(window, vals)

def save_file_as(window, vals) -> str:

    try:
        filename: str = sg.popup_get_file('Save File', save_as=True, no_window=True)
    except:
        return
    if filename not in (None, '') and not isinstance(filename, tuple):
        with open(filename,'w') as f:
            f.write(vals.get('_BODY_'))
        window['_INFO_'].update(value=filename)
    return filename