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

    data = response.json()
    return response.json()


# -------------------------
# SAFE MATCH ODDS
# -------------------------
def normalize(name):
    return name.lower().strip()


def get_match_odds(home, away, odds_data):

    home_n = normalize(home)
    away_n = normalize(away)

    for game in odds_data:

        game_home = normalize(game.get("home_team", ""))
        game_away = normalize(game.get("away_team", ""))

        # flexibel matchning
        if (home_n == game_home and away_n == game_away) or \
           (home_n == game_away and away_n == game_home):

            outcomes = game["bookmakers"][0]["markets"][0]["outcomes"]

           # odds_map = {
          #      normalize(o["name"]): o["price"]
           #     for o in outcomes
           # }

            odds_map = {}

               for o in outcomes:

               if normalize(o["name"]) == game_home:
               odds_map["home"] = o["price"]

               elif normalize(o["name"]) == game_away:
               odds_map["away"] = o["price"]

               else:
               odds_map["draw"] = o["price"]

               return odds_map

    return None
