import math

HOME_ADVANTAGE = 0
K_FACTOR = 32

# -------------------------
# DYNAMISK ELO STORE
# -------------------------
# TEAM_ELO = {}
TEAM_ELO = {
    "Spain": 2050,
    "United States": 2000,
    "England": 1980,
    "Germany": 1950,
    "France": 1930,
    "Sweden": 1910,
    "Japan": 1890,
    "Brazil": 1870,
    "Netherlands": 1860,
    "Norway": 1820,
    "Australia": 1800,
    "Italy": 1790,
    "Canada": 1780,
    "Denmark": 1770,
    "Switzerland": 1740,
    "Belgium": 1710,
    "Colombia": 1850,
    "Argentina": 1700,
    "Egypt": 1600
}

# -------------------------
# GET / INIT ELO
# -------------------------
def get_elo(team):

    if team not in TEAM_ELO:
        TEAM_ELO[team] = 1500  # startvärde

    return TEAM_ELO[team]


# -------------------------
# EXPECTED SCORE
# -------------------------
def expected_score(home_elo, away_elo):

    adjusted_home = home_elo + HOME_ADVANTAGE

    return 1 / (1 + 10 ** ((away_elo - adjusted_home) / 400))


# -------------------------
# PROBABILITIES
# -------------------------
def get_probabilities(home_team, away_team):

    home_elo = get_elo(home_team)
    away_elo = get_elo(away_team)

    home_win = expected_score(home_elo, away_elo)

    draw = 0.25

    home_win = home_win * 0.75
    away_win = max(0, 1 - home_win - draw)

    total = home_win + draw + away_win

    return {
        "home": home_win / total,
        "draw": draw / total,
        "away": away_win / total
    }


# -------------------------
# UPDATE ELO AFTER MATCH
# -------------------------
def update_elo(home_team, away_team, result):
    """
    result: "home", "away", "draw"
    """

    home_elo = get_elo(home_team)
    away_elo = get_elo(away_team)

    expected_home = expected_score(home_elo, away_elo)
    expected_away = 1 - expected_home

    if result == "home":
        score_home, score_away = 1, 0
    elif result == "away":
        score_home, score_away = 0, 1
    else:
        score_home, score_away = 0.5, 0.5

    TEAM_ELO[home_team] = home_elo + K_FACTOR * (score_home - expected_home)
    TEAM_ELO[away_team] = away_elo + K_FACTOR * (score_away - expected_away)

def process_match_result(home_team, away_team, home_score, away_score):

    if home_score > away_score:
        result = "home"
    elif away_score > home_score:
        result = "away"
    else:
        result = "draw"

    update_elo(home_team, away_team, result)


# -------------------------
# EV
# -------------------------
def calculate_ev(probability, odds):
    return (probability * odds) - 1


# -------------------------
# KELLY
# -------------------------
def kelly(probability, odds):

    b = odds - 1
    q = 1 - probability

    if b <= 0:
        return 0

    k = (probability * b - q) / b

    return max(0, k)


# -------------------------
# ARBITRAGE
# -------------------------
def detect_arbitrage(odds):

    try:
        total = (
            1 / odds["home"] +
            1 / odds["draw"] +
            1 / odds["away"]
        )

        return total < 1

    except:
        return False
