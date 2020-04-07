"""
Module that handles saving and loading application data.
"""

import os.path
import pickle


SAVEFILE = os.path.join(os.path.curdir, "modules", "appdata.bin")

def load(file_name=SAVEFILE):
    """
    Depicles object saved in 'file_name' and returns it. If the file doesn't exist, returns None.  
    file_name [str] - defaults to 'appdata.pickle'
    """
    if not os.path.isfile(file_name) or os.path.getsize(file_name) < 1:
        return None

    with open(file_name, "rb") as file:
        loaded_object = pickle.load(file)
    return loaded_object


def save(object, file_name=SAVEFILE):
    "Pickles passed object to 'file_name'."
    with open(file_name, "wb") as file:
        pickle.dump(object, file, -1)
