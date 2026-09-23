import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime

TEAM_URL = "https://www.espn.co.uk/football/team/fixtures/_/id/357"  # Stockport County

def fetch():
    r = requests.get(TEAM_URL, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    events = []

    # ESPN fixture rows
    rows = soup.select("table tbody tr")

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 3:
            continue

        date_text = cols[0].get_text(strip=True)
        opponent = cols[1].get_text(strip=True)
        comp = cols[2].get_text(strip=True)

        # Convert date
        try:
            dt = datetime.strptime(date_text, "%a, %d %b %Y")
            iso_date = dt.isoformat() + "Z"
        except:
            continue

        events.append({
            "date": iso_date,
            "opponent": opponent,
            "competition": comp,
        })

    with open("stockport.json", "w") as f:
        json.dump({"events": events}, f, indent=2)

if __name__ == "__main__":
    fetch()
