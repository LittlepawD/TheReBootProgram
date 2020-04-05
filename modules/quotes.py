import random as rn
import json
import os


# TODO: Change the ubication of the json file


def quotes_load():

    # This function loads the json file and add it to a variable named quotes
    if os.path.isfile("./modules/quotes.json") and os.stat("./modules/quotes.json").st_size != 0:
        old_file = open("./modules/quotes.json", "r+")
        data = json.loads(old_file.read())
        quotes = rn.choice(list(data["quotes"]))
        return quotes

    # TODO: Change the way of how the project generates a json,
    #       right now is only for development purposes.

    else:
        # You need to run this is you delete quotes.json
        old_file = open("./modules/quotes.json", "w+")
        data = {"quotes": ["Success is the sum of small efforts, repeated day after day.",
                           "You can do it!"]}
        old_file.seek(0)
        old_file.write(json.dumps(data))


class QuotesData:
    pass
