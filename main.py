import os
import requests
from fastapi import FastAPI

app = FastAPI()

API_KEY = os.getenv("API_KEY")

headers = {
    "X-Auth-Token": API_KEY
}

@app.get("/matches")
def get_matches():

    url = "https://api.football-data.org/v4/matches"
    response = requests.get(url, headers=headers)

    data = response.json()["matches"]

    result = []

    for m in data[:10]:

        home = m["homeTeam"]["name"]
        away = m["awayTeam"]["name"]

        # 🔧 tillfälliga odds (sen ersätter vi med riktiga)
        home_odds = 2.20

        # 🎲 enkel sannolikhetsmodell
        home_prob = 0.45

        # 💰 EV-beräkning
        ev = calculate_ev(home_prob, home_odds)

        result.append({
            "home": home,
            "away": away,
            "home_probability": home_prob,
            "home_odds": home_odds,
            "ev": round(ev, 3)
        })

    return result

def calculate_ev(probability, odds):
    return (probability * odds) - 1
