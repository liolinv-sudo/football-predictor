import os
import requests
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from predictor import get_probabilities, calculate_ev, kelly
from odds import fetch_odds, get_match_odds

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

API_KEY = os.getenv("API_KEY")
ODDS_API_KEY = os.getenv("ODDS_API_KEY")


@app.get("/")
def root():
    return FileResponse("frontend/index.html")


@app.get("/matches")
def get_matches():

    matches = requests.get(
        "https://api.football-data.org/v4/matches",
        headers={"X-Auth-Token": API_KEY}
    ).json()["matches"]

    odds_data = fetch_odds()

    result = []

    for m in matches[:15]:

        home = m["homeTeam"]["name"]
        away = m["awayTeam"]["name"]

        probs = get_probabilities(home, away)
        odds = get_match_odds(home, away, odds_data)

        if not odds:
            continue

        ev = calculate_ev(probs["home"], odds[home])

        if ev > 0:

            kelly_value = kelly(probs["home"], odds[home])

            result.append({
                "home": home,
                "away": away,
                "ev": round(ev, 3),
                "odds": odds,
                "kelly": round(kelly_value, 3)
            })

    result.sort(key=lambda x: x["ev"], reverse=True)

    return result


app.mount(
    "/frontend",
    StaticFiles(directory=os.path.join(BASE_DIR, "frontend")),
    name="frontend"
)
