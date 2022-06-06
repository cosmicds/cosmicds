import json
from os.path import exists, dirname, join, realpath

def load_style(name):
    filename = f"{name}.json"
    directory = dirname(realpath(__file__))
    filepath = join(directory, filename)
    try:
        if exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
    except:
        return None
