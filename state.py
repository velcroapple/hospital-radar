import json
import os

SEEN_PATH = "data/seen.json"


def load_seen():
    if not os.path.exists(SEEN_PATH):
        return set()
    with open(SEEN_PATH, "r") as f:
        return set(json.load(f))


def save_seen(seen):
    os.makedirs(os.path.dirname(SEEN_PATH), exist_ok=True)
    with open(SEEN_PATH, "w") as f:
        json.dump(list(seen), f, indent=2)