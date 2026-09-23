import requests
import json
from datetime import datetime
import pytz

# ESPN endpoint (UK edition)
URL = "https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/teams/364/schedule"

def fetch():
    r = requests.get(URL, timeout=10)
    data = r.json()

    events = []

    for e in data.get("events", []):
        try:
            events.append({
                "id": e.get("id"),
                "date": e.get("date"),
                "name": e.get("name"),
                "shortName": e.get("shortName"),
                "competition": e["competitions"][0]["name"],
                "venue": {
                    "fullName": e["competitions"][0]["venue"]["fullName"],
                    "city": e["competitions"][0]["venue"].get("address", {}).get("city", ""),
                    "country": e["competitions"][0]["venue"].get("address", {}).get("country", "")
                },
                "competitors": [
                    {
                        "id": c["id"],
                        "homeAway": c["homeAway"],
                        "displayName": c["displayName"],
                        "abbreviation": c["abbreviation"],
                        "logo": c["logo"]
                    }
                    for c in e["competitions"][0]["competitors"]
                ],
                "links": {
                    "summary": e["links"][0]["href"] if e.get("links") else ""
                }
            })
        except Exception:
            # fallback for friendlies / incomplete metadata
            events.append({
                "id": f"friendly-{len(events)}",
                "date": "TBD",
                "name": e.get("name", "Friendly"),
                "shortName": e.get("shortName", "FRI"),
                "competition": "Friendly",
                "venue": {"fullName": "TBD"},
                "competitors": [],
                "links": {"summary": ""}
            })

    # Sort by date (TBD stays at bottom)
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
