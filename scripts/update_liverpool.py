import requests
import json
from datetime import datetime

# ESPN Premier League – Liverpool (team ID 364)
URL = "https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/teams/364/schedule"

def fetch():
    r = requests.get(URL, timeout=10)
    data = r.json()

    events = []

    for e in data.get("events", []):
        try:
            comp = e["competitions"][0]
            venue = comp.get("venue", {})
            address = venue.get("address", {})

            events.append({
                "id": e.get("id"),
                "date": e.get("date"),
                "name": e.get("name"),
                "shortName": e.get("shortName"),
                "competition": comp.get("name"),
                "venue": {
                    "fullName": venue.get("fullName", ""),
                    "city": address.get("city", ""),
                    "country": address.get("country", "")
                },
                "competitors": [
                    {
                        "id": c.get("id"),
                        "homeAway": c.get("homeAway"),
                        "displayName": c.get("displayName"),
                        "abbreviation": c.get("abbreviation"),
                        "logo": c.get("logo")
                    }
                    for c in comp.get("competitors", [])
                ],
                "links": {
                    "summary": e["links"][0]["href"] if e.get("links") else ""
                }
            })
        except Exception:
            continue

    def sort_key(ev):
        try:
            return datetime.fromisoformat(ev["date"].replace("Z", "+00:00"))
        except:
            return datetime.max

    events.sort(key=sort_key)

    with open("liverpool.json", "w") as f:
        json.dump({"events": events}, f, indent=2)

if __name__ == "__main__":
    fetch()
