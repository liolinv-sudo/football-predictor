import math

HOME_ADVANTAGE = 75

def expected_score(home_elo, away_elo):

    adjusted_home = home_elo + HOME_ADVANTAGE

    return 1 / (
        1 + 10 ** (
            (away_elo - adjusted_home) / 400
        )
    )
