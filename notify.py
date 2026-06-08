import os
import requests

TOPIC = os.environ["NTFY_TOPIC"]


def send_ntfy(title, message):
    requests.post(
        f"https://ntfy.sh/{TOPIC}",
        data=message.encode("utf-8"),
        headers={
            "Title": title,
            "Priority": "default",
            "Tags": "hospital"
        },
        timeout=30,
    )