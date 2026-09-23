import requests
import json
from datetime import datetime

URL = "https://www.scorebat.com/api/competition/england-league-one/"

def fetch():
    r = requests.get(URL, timeout=10)
    data = r.json()

    events = []

    for match in data.get("matches", []):
        # Only include Stockport County fixtures
        if "Stockport" not in (match.get("home_team", "") + match.get("away_team", "")):
            continue

        events.append({
            "id": match.get("id"),
            "date": match.get("date"),
            "homeTeam": match.get("home_team"),
            "awayTeam": match.get("away_team"),
            "competition": "League One",
            "venue": match.get("venue", ""),
            "status": match.get("status", "")
        })

    # Sort by date
    events.sort(key=lambda x: datetime.fromisoformat(x["date"].replace("Z", "+00:00")))

    with open("stockport.json", "w") as f:
        json.dump({"events": events}, f, indent=2)

if __name__ == "__main__":
    fetch()
