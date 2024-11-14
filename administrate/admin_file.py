import pickle
import os

home = os.path.dirname(__file__)


def get_admins():
    with open(f'{home}/admins.txt', 'rb') as f:
        return pickle.load(f)
    

def add_admin(data):
    with open(f'{home}/admins.txt', 'wb') as f:
        pickle.dump(data, f)


