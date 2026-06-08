import requests


TOPIC = "hospital-radar-7f3a91"


def send_ntfy(title, message):

    requests.post(
        f"https://ntfy.sh/{TOPIC}",
        data=message.encode("utf-8"),
        headers={
            "Title": title,
            "Priority": "default",
            "Tags": "hospital"
        }
    )
