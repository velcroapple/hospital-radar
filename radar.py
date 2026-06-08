from sources import get_rghs
from state import load_seen, save_seen
import hashlib


def get_event_id(event):
    return hashlib.sha1(
        event["pdf_link"].encode()
    ).hexdigest()


seen = load_seen()

events = get_rghs()

new_count = 0

for event in events:

    event_id = get_event_id(event)

    if event_id not in seen:

        print("NEW:", event["title"])

        seen.add(event_id)

        new_count += 1

save_seen(seen)

print()
print("New events:", new_count)