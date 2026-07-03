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

    for m in data[:15]:  # begränsa först

        result.append({
            "home": m["homeTeam"]["name"],
            "away": m["awayTeam"]["name"],
            "competition": m["competition"]["name"],
            "status": m["status"]
        })

    return result
