import os
import json


home = os.path.dirname(__file__)


def get_amounts():
    with open(f'{home}/price.json', 'r', encoding="utf-8") as f:
        return json.load(f)
    

def set_amounts(data):
    with open(f'{home}/price.json', 'w', encoding="utf-8") as f:
        return json.dump(data, f)

    

