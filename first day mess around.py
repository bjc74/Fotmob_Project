from statsbombpy import sb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
competitions = sb.competitions()
competitions = competitions.drop(columns = ['match_updated_360', 'match_available_360', 'match_updated'])
matches = sb.matches(competition_id = 9, season_id = 281)
#print(competitions.head())
#print(matches.head())
#print(matches.columns)
#print(lineups)
#print(events)
def match_stats(matchid):
    lineups = sb.lineups(match_id = matchid)
    events = sb.events(match_id = matchid)
    events = events.dropna(how = 'all', axis = 1)
    teams = list(lineups.keys())
    team1 = teams[0]
    team2 = teams[1]
    shots = events[events["type"] == "Shot"]
    shots = shots.dropna(how = 'all', axis = 1)
    shots_useful_info = shots[["player", "minute", "shot_outcome", "team"]]
    shots_per_team = shots["team"].value_counts()
    passes = events[events["type"] == "Pass"]
    passes = passes.dropna(how = 'all', axis = 1)
    passes_by_team = passes["team"].value_counts()
    events_by_player = events["player"].value_counts()
    top_5_players_by_events = events_by_player.head()
    team1_shots = shots_per_team.get(team1, 0)
    team2_shots = shots_per_team.get(team2, 0)
    team1_passes = passes_by_team.get(team1, 0)
    team2_passes = passes_by_team.get(team2, 0)
    goals = shots_useful_info[shots_useful_info["shot_outcome"] == "Goal"]
    goals = goals.dropna(how = 'all')
    team_goals = goals.value_counts(["team"])
    team1_score = team_goals.get(team1, 0)
    team2_score = team_goals.get(team2, 0)
    print(f"{team1} {team1_score} - {team2_score} {team2}")
    print(f"\nShots per team: \n{team1}: {team1_shots}\n{team2}: {team2_shots}")
    print(f"\nPasses per team: \n{team1}: {team1_passes}\n{team2}: {team2_passes}")
    print(f"\nTop 5 Players by events: {top_5_players_by_events}")
    return
match_stats(3895292)

