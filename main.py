from fastapi import FastAPI

app = FastAPI()

matches = [
    {
        "home": "Malmö FF",
        "away": "AIK",
        "home_win": 45,
        "draw": 28,
        "away_win": 27
    },
    {
        "home": "Hammarby",
        "away": "Djurgården",
        "home_win": 39,
        "draw": 30,
        "away_win": 31
    }
]

@app.get("/")
def root():
    return {"message": "Football Predictor"}

@app.get("/matches")
def get_matches():
    return matches
