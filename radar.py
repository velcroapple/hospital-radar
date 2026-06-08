from sources import get_rghs, get_rajswasthya_circulars
from state import load_seen, save_seen
import hashlib
from notify import send_ntfy


def classify(event):
    title = event["title"].lower()
    if any(word in title for word in [
        "claim",
        "cashless",
        "reimbursement",
        "empanelment",
        "tat"
    ]):
        return "Revenue"
    if any(word in title for word in [
        "inspection",
        "audit",
        "cctv",
        "nsq"
    ]):
        return "Compliance"
    if any(word in event["title"] for word in [
        "नेत्र",
        "अंधता",
        "मोतियाबिंद",
        "शिविर"
    ]):
        return "Growth"
    return "General"


def get_event_id(event):
    key = event.get("pdf_link") or f"{event['title']}|{event['date']}"
    return hashlib.sha1(key.encode()).hexdigest()


seen = load_seen()

rghs = get_rghs()
raj = get_rajswasthya_circulars()
events = rghs + raj

new_count = 0
for event in events:
    event_id = get_event_id(event)
    if event_id not in seen:
        print("NEW:", event["title"])
        category = classify(event)
        if category != "General":
            send_ntfy(
                f"{category} | {event['source']}",
                f"{event['title']}\n\n{event['date']}"
            )

        seen.add(event_id)
        new_count += 1

save_seen(seen)

print()
print(f"RGHS events: {len(rghs)}")
print(f"RajSwasthya events: {len(raj)}")
print(f"Total events: {len(events)}")
print(f"New events: {new_count}")