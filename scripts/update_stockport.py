import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://www.espn.co.uk/football/team/fixtures/_/id/357"

def fetch():
    r = requests.get(URL, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    events = []

    # ESPN uses multiple tables, one per month
    tables = soup.find_all("table")

    for table in tables:
        rows = table.find_all("tr")

        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 4:
                continue

            date_text = cols[0].get_text(strip=True)
            match_text = cols[1].get_text(strip=True)
            time_text = cols[2].get_text(strip=True)
            comp_text = cols[3].get_text(strip=True)

            # Convert date
            try:
                dt = datetime.strptime(date_text, "%a, %d %b %Y")
                iso_date = dt.isoformat() + "Z"
            except:
                continue

            events.append({
                "date": iso_date,
                "match": match_text,
                "time": time_text,
                "competition": comp_text
            })

    with open("stockport.json", "w") as f:
        json.dump({"events": events}, f, indent=2)

if __name__ == "__main__":
    fetch()
