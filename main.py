import os
import requests
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from odds import fetch_odds, get_match_odds
from predictor import (
    get_probabilities,
    calculate_ev,
    kelly,
    process_match_result
)

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

API_KEY = os.getenv("API_KEY")


# -------------------------
# FRONTEND (dashboard)
# -------------------------
@app.get("/")
def root():
    return FileResponse(os.path.join(BASE_DIR, "frontend", "index.html"))


# -------------------------
# ODDS + MATCH DATA
# -------------------------
FOOTBALL_URL = "https://api.football-data.org/v4/matches"


@app.get("/matches")
def get_matches():

    # Hämta matcher
    response = requests.get(
        FOOTBALL_URL,
        headers={"X-Auth-Token": API_KEY}
    )

    matches = response.json().get("matches", [])

    # Hämta odds
    odds_data = fetch_odds()

    result = []

    for m in matches[:15]:

        home = m["homeTeam"]["name"]
        away = m["awayTeam"]["name"]

        # sannolikhet (Elo)
        probs = get_probabilities(home, away)

        # odds-matchning
        odds = get_match_odds(home, away, odds_data)
        print("MATCH:", home, "-", away)
        print("ODDS:", odds)

        if not odds:
            continue

        home_odds = odds.get(home)
        print("HOME_ODDS:", home_odds)

        if not home_odds:
            continue

        # EV
        ev = calculate_ev(probs["home"], home_odds)

        # endast +EV spel
        if ev <= 0:
            continue

        # Kelly
        kelly_value = kelly(probs["home"], home_odds)

        result.append({
            "home": home,
            "away": away,
            "ev": round(ev, 3),
            "odds": odds,
            "kelly": round(kelly_value, 3)
        })

    # sortera bästa spel först
    result.sort(key=lambda x: x["ev"], reverse=True)

    return result

@app.post("/result")
def add_result(data: dict):

    home = data["home"]
    away = data["away"]
    home_score = data["home_score"]
    away_score = data["away_score"]

    process_match_result(home, away, home_score, away_score)

    return {"status": "Elo updated"}

app.mount(
    "/frontend",
    StaticFiles(directory=os.path.join(BASE_DIR, "frontend")),
    name="frontend"
)
