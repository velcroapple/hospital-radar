import requests
from bs4 import BeautifulSoup


def get_rghs():
    url = "https://rghs.rajasthan.gov.in/RGHS/home/circularNotice"

    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table")

    events = []

    rows = table.find_all("tr")[1:]  # skip header

    for row in rows:
        cols = row.find_all("td")

        if len(cols) < 6:
            continue

        pdf_link = None

        download_cell = cols[5]

        link = download_cell.find("a")

        if link:
            pdf_link = link.get("href")

        event = {
            "date": cols[1].get_text(strip=True),
            "type": cols[2].get_text(strip=True),
            "title": cols[3].get_text(strip=True),
            "issued_by": cols[4].get_text(strip=True),
            "pdf_link": pdf_link,
        }

        events.append(event)

    return events