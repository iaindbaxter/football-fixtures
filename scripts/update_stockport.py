import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://www.bbc.co.uk/sport/football/teams/stockport-county/scores-fixtures"

def fetch():
    r = requests.get(URL, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "lxml")

    events = []

    # BBC fixtures are inside <li class="gs-o-list-ui__item gs-u-pb++">
    fixtures = soup.find_all("li", class_="gs-o-list-ui__item gs-u-pb++")

    for f in fixtures:
        date_el = f.find("time")
        if not date_el:
            continue

        date_iso = date_el.get("datetime")

        teams = f.find_all("span", class_="sp-c-fixture__team-name")
        if len(teams) != 2:
            continue

        home = teams[0].get_text(strip=True)
        away = teams[1].get_text(strip=True)

        comp_el = f.find("span", class_="sp-c-fixture__competition")
        competition = comp_el.get_text(strip=True) if comp_el else ""

        events.append({
            "date": date_iso,
            "homeTeam": home,
            "awayTeam": away,
            "competition": competition
        })

    with open("stockport.json", "w") as f:
        json.dump({"events": events}, f, indent=2)

if __name__ == "__main__":
    fetch()
