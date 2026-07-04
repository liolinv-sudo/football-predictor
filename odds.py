import os
import requests

ODDS_API_KEY = os.getenv("ODDS_API_KEY")


def fetch_odds():

    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"

    params = {
        "apiKey": ODDS_API_KEY,
        "regions": "eu",
        "markets": "h2h"
    }

    r = requests.get(url, params=params)
    return r.json()

def get_match_odds(home, away, odds_data):

    for game in odds_data:

        if game["home_team"] == home and game["away_team"] == away:

            outcomes = game["bookmakers"][0]["markets"][0]["outcomes"]

            return {
                o["name"]: o["price"] for o in outcomes
            }

    return None
