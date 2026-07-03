from fastapi import FastAPI

app = FastAPI()

matches = [
    {
        "home": "Malmö FF",
        "away": "AIK",
        "home_probability": 0.45,
        "home_odds": 2.50
    }
]

@app.get("/")
def root():
    return {"message": "Football Predictor"}

@app.get("/matches")
def get_matches():

    result = []

    for match in matches:

        ev = (match["home_probability"] * match["home_odds"]) - 1

        result.append({
            "home": match["home"],
            "away": match["away"],
            "probability": match["home_probability"],
            "odds": match["home_odds"],
            "ev": round(ev, 3)
        })

    return result
