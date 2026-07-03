import math

HOME_ADVANTAGE = 75

def expected_score(home_elo, away_elo):

    adjusted_home = home_elo + HOME_ADVANTAGE

    return 1 / (
        1 + 10 ** (
            (away_elo - adjusted_home) / 400
        )
    )

def probabilities(home_elo, away_elo):

    home_win = expected_score(home_elo, away_elo)

    draw = 0.25

    home_win *= 0.75
    away_win = (1 - home_win - draw)

    return {
        "home": round(home_win, 3),
        "draw": round(draw, 3),
        "away": round(away_win, 3)
    }
