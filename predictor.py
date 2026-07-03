import math

def expected_score(home_elo, away_elo):

    return 1 / (
        1 + math.pow(
            10,
            (away_elo - home_elo) / 400
        )
    )
