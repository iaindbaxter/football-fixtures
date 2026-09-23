import requests
import json
from datetime import datetime

URL = "https://www.football-data.org/v4/teams/357/matches?status=SCHEDULED"

def fetch():
    r = requests.get(URL, timeout=10)
    data = r.json()

    events = []

    for m in data.get("matches", []):
        events.append({
            "id": m.get("id"),
            "utcDate": m.get("utcDate"),
            "status": m.get("status"),
            "matchday": m.get("matchday"),
            "homeTeam": m.get("homeTeam", {}).get("name"),
            "awayTeam": m.get("awayTeam", {}).get("name"),
            "competition": m.get("competition", {}).get("name"),
            "venue": m.get("venue", None),
        })

    events.sort(key=lambda x: datetime.fromisoformat(x["utcDate"].replace("Z", "+00:00")))

    with open("stockport.json", "w") as f:
        json.dump({"events": events}, f, indent=2)

if __name__ == "__main__":
    fetch()
