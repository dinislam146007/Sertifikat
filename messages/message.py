import os

home = os.path.dirname(__file__)


def get_inf() -> int:
    with open(f"{home}/inf.txt", "r", encoding="utf-8") as f:
        return f.read()


def get_services() -> int:
    with open(f"{home}/services.txt", "r", encoding="utf-8") as f:
        return f.read()


def set_services(new_services):
    with open(f"{home}/services.txt", "w", encoding="utf-8") as f:
        f.write(new_services)


def set_inf(new_inf):
    with open(f"{home}/inf.txt", "w", encoding="utf-8") as f:
        f.write(new_inf)