import math
from data import TEAM_ELO

HOME_ADVANTAGE = 75


# -------------------------
# ELO EXPECTED SCORE
# -------------------------
def expected_score(home_elo, away_elo):

    adjusted_home = home_elo + HOME_ADVANTAGE

    return 1 / (1 + 10 ** ((away_elo - adjusted_home) / 400))


# -------------------------
# PROBABILITIES (MVP MODEL)
# -------------------------
def get_probabilities(home_team, away_team):

    home_elo = TEAM_ELO.get(home_team, 1500)
    away_elo = TEAM_ELO.get(away_team, 1500)

    home_win = expected_score(home_elo, away_elo)

    # draw baseline (MVP antagande)
    draw = 0.25

    # justera så att total inte blir > 1
    home_win = home_win * 0.75
    away_win = max(0, 1 - home_win - draw)

    # normalisera (säkerhet)
    total = home_win + draw + away_win

    return {
        "home": round(home_win / total, 3),
        "draw": round(draw / total, 3),
        "away": round(away_win / total, 3)
    }


# -------------------------
# EXPECTED VALUE
# -------------------------
def calculate_ev(probability, odds):

    return (probability * odds) - 1


# -------------------------
# KELLY CRITERION
# -------------------------
def kelly(probability, odds):

    b = odds - 1
    q = 1 - probability

    kelly_value = (probability * b - q) / b

    return max(0, kelly_value)
