import os
import json
from main import home


def get_amounts():
    with open(f'{home}/amount/price.json') as f:
        return json.load(f)
    

