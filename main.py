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
    process_match_result,
    detect_arbitrage
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

    print("=== GET_MATCHES CALLED ===")

    response = requests.get(
        FOOTBALL_URL,
        headers={"X-Auth-Token": API_KEY}
    )
    print(response.url)
    print(response.status_code)
    print(response.text[:1000])

    matches = response.json().get("matches", [])
    print("Matches fetched:", len(matches))

    odds_data = fetch_odds()

    result = []

    for m in matches[:15]:

        home = m["homeTeam"]["name"]
        away = m["awayTeam"]["name"]

        probs = get_probabilities(home, away)

        print("PROBS:", probs)

        odds = get_match_odds(home, away, odds_data)

        print("MATCH:", home, "-", away)
        print("ODDS:", odds)

        if not odds:
            continue

        arb = detect_arbitrage(odds)

        # Säkerställ att alla odds finns
        if (
            odds.get("home") is None
            or odds.get("draw") is None
            or odds.get("away") is None
        ):
            continue

        # EV för alla utfall
        ev_home = calculate_ev(
            probs["home"],
            odds["home"]
        )

        ev_draw = calculate_ev(
            probs["draw"],
            odds["draw"]
        )

        ev_away = calculate_ev(
            probs["away"],
            odds["away"]
        )

        best_ev = max(
            ev_home,
            ev_draw,
            ev_away
        )

        print("EV_HOME:", ev_home)
        print("EV_DRAW:", ev_draw)
        print("EV_AWAY:", ev_away)
        print("BEST_EV:", best_ev)

        if best_ev == ev_home:
            bet = "home"
            best_prob = probs["home"]
            best_odds = odds["home"]

        elif best_ev == ev_draw:
            bet = "draw"
            best_prob = probs["draw"]
            best_odds = odds["draw"]

        else:
            bet = "away"
            best_prob = probs["away"]
            best_odds = odds["away"]

        if best_ev <= 0:
            continue

        kelly_value = kelly(
            best_prob,
            best_odds
        )

        result.append({
            "home": home,
            "away": away,
            "bet": bet,
            "ev": round(best_ev, 3),
            "kelly": round(kelly_value, 3),
            "arbitrage": arb,
            "odds": odds
        })

    result.sort(
        key=lambda x: x["ev"],
        reverse=True
    )

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
