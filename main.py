import os
import requests
from fastapi import FastAPI
from predictor import probabilities
from data import TEAM_ELO

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

@app.get("/matches")
def get_matches():

    matches = requests.get(
        "https://api.football-data.org/v4/matches",
        headers=headers
    ).json()["matches"]

    odds_data = fetch_odds()

    result = []

    for m in matches[:10]:

        odds = get_best_odds(m, odds_data)

        if not odds:
            continue

        home = m["homeTeam"]["name"]

        home_prob = 0.45  # (sen förbättrar vi modellen)

        ev = calculate_ev(home_prob, odds[home])

        result.append({
            "home": home,
            "away": m["awayTeam"]["name"],
            "odds": odds,
            "home_probability": home_prob,
            "ev": round(ev, 3)
        })

    return result

def calculate_ev(probability, odds):
    return (probability * odds) - 1
