import json


def load_seen():
    with open("data/seen.json", "r") as f:
        return set(json.load(f))


def save_seen(seen):
    with open("data/seen.json", "w") as f:
        json.dump(list(seen), f, indent=2)