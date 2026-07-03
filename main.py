from fastapi import FastAPI
import requests

app = FastAPI()

API_KEY = "70054ffca7094d3dbec1f83b18d10b67"

headers = {
    "X-Auth-Token": API_KEY
}

def fetch_matches():
    url = "https://api.football-data.org/v4/matches"
    response = requests.get(url, headers=headers)
    return response.json()["matches"]


@app.get("/")
def root():
    return {"message": "Football Predictor"}


@app.get("/matches")
def get_matches():

    raw = fetch_matches()

    result = []

    for m in raw[:10]:

        home = m["homeTeam"]["name"]
        away = m["awayTeam"]["name"]

        result.append({
            "home": home,
            "away": away
        })

    return result
