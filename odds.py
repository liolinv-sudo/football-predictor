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
