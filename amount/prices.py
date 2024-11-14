import os
import json


home = os.path.dirname(__file__)


def get_amounts():
    with open(f'{home}/amount/price.json') as f:
        return json.load(f)
    

