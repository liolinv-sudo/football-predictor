import os
import requests

ODDS_API_KEY = os.getenv("ODDS_API_KEY")

BASE_URL = "https://api.the-odds-api.com/v4/sports/soccer/odds/"


# -------------------------
# FETCH ODDS
# -------------------------
def fetch_odds():

    if not ODDS_API_KEY:
        raise Exception("Missing ODDS_API_KEY")

    params = {
        "apiKey": ODDS_API_KEY,
        "regions": "eu",
        "markets": "h2h",
        "oddsFormat": "decimal"
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        return []

    return response.json()


# -------------------------
# SAFE MATCH ODDS
# -------------------------
def get_match_odds(home, away, odds_data):

    if not odds_data:
        return None

    for game in odds_data:

        try:
            if game.get("home_team") != home:
                continue

            if game.get("away_team") != away:
                continue

            bookmakers = game.get("bookmakers", [])
            if not bookmakers:
                continue

            markets = bookmakers[0].get("markets", [])
            if not markets:
                continue

            outcomes = markets[0].get("outcomes", [])
            if not outcomes:
                continue

            return {
                o["name"]: o["price"]
                for o in outcomes
            }

        except Exception:
            continue

    return None
