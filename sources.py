import requests
import re
from bs4 import BeautifulSoup


def get_rghs():
    url = "https://rghs.rajasthan.gov.in/RGHS/home/circularNotice"
    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30,
    )
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    if table is None:
        return []
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
            "source": "RGHS",
            "date": cols[1].get_text(strip=True),
            "type": cols[2].get_text(strip=True),
            "title": cols[3].get_text(strip=True),
            "issued_by": cols[4].get_text(strip=True),
            "pdf_link": pdf_link,
        }
        events.append(event)
    return events


def get_rajswasthya_circulars():
    url = "https://rajswasthya.rajasthan.gov.in/link/fetch_data2.php"
    response = requests.post(
        url,
        data={
            "draw": 1,
            "start": 0,
            "length": 100
        },
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=30,
    )
    data = response.json()
    events = []
    for row in data["data"]:
        html = row["title"]
        soup = BeautifulSoup(html, "html.parser")
        title = soup.get_text(strip=True)
        link = soup.find("a")
        onclick = link.get("onclick", "")
        match = re.search(r"openPDF\('([^']+)'\)", onclick)
        if not match:
            continue
        pdf_path = match.group(1)
        pdf_url = (
            "https://rajswasthya.rajasthan.gov.in/"
            + pdf_path.replace("../", "")
        )
        event = {
            "source": "RajSwasthya",
            "title": title,
            "date": row["date"],
            "pdf_link": pdf_url
        }
        events.append(event)
    return events