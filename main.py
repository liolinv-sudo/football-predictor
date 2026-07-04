import os
import requests
from fastapi import FastAPI
from predictor import probabilities
from odds import fetch_odds, get_match_odds

app = FastAPI()

API_KEY = os.getenv("API_KEY")

ODDS_API_KEY = os.getenv("ODDS_API_KEY")

def fetch_odds():

    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"

    params = {
        "apiKey": ODDS_API_KEY,
        "regions": "eu",
        "markets": "h2h"
    }

    response = requests.get(url, params=params)
    return response.json()

def get_best_odds(match, odds_data):

    for game in odds_data:

        if (game["home_team"] == match["homeTeam"]["name"] and
            game["away_team"] == match["awayTeam"]["name"]):

            outcomes = game["bookmakers"][0]["markets"][0]["outcomes"]

            return {
                outcome["name"]: outcome["price"]
                for outcome in outcomes
            }

    return None




headers = {
    "X-Auth-Token": API_KEY
}

#@app.get("/matches")
#def get_matches():

  @app.get("/matches")
def get_matches():

    matches = requests.get(
        "https://api.football-data.org/v4/matches",
        headers={"X-Auth-Token": os.getenv("API_KEY")}
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

        # 🔥 FILTER: visa bara +EV
        if ev > 0:

            result.append({
                "home": home,
                "away": away,
                "odds": odds,
                "probabilities": probs,
                "ev": round(ev, 3)
            })

    # 🔥 SORTERA bästa först
    result.sort(key=lambda x: x["ev"], reverse=True)

    return result

def calculate_ev(probability, odds):
    return (probability * odds) - 1
