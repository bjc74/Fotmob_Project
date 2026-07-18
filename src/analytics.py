import pandas as pd
import os
from statsbombpy import sb
def load_match_data(match_id):
    lineups = sb.lineups(match_id = match_id)
    events = sb.events(match_id = match_id)
    events = events.dropna(how = 'all', axis = 1)
    teams = list(lineups.keys())
    team1 = teams[0]
    team2 = teams[1]
    return lineups, events, team1, team2
def get_score(events, team1, team2):
    team1_goals, team2_goals = count_shot_outcome_by_team("Goal", events, team1, team2)
    team1_own_goals_for, team2_own_goals_for = count_events_by_team("Own Goal For", events, team1, team2)
    return(team1_goals + team1_own_goals_for), (team2_goals + team2_own_goals_for)
def count_events_by_team(event, events, team1, team2):
    event_everyone = events[events["type"] == event]
    event_by_team = event_everyone["team"].value_counts()
    team1_count = event_by_team.get(team1, 0)
    team2_count = event_by_team.get(team2, 0)
    return team1_count, team2_count
def count_events_by_player(event, events):
    event = events[events["type"] == event]
    event_by_player = event["player"].value_counts()
    return event_by_player
def get_top_players_by_events(events, n):
    #Series with named index + reset_index = DataFrame
    events_by_player = events["player"].value_counts()
    events_by_player = events_by_player.head(n)
    events_by_player = events_by_player.rename_axis("player")
    events_by_player = events_by_player.reset_index(name = "events")
    return events_by_player
def count_shot_outcome_by_team(shot_type, events, team1, team2):
    shots = events[events["type"] == "Shot"]
    goals = shots[shots["shot_outcome"] == shot_type]
    goals_by_team = goals["team"].value_counts()
    team1_score = goals_by_team.get(team1, 0)
    team2_score = goals_by_team.get(team2, 0)
    return team1_score, team2_score
def get_xg_stats(events):
    shots = events[events["type"] == "Shot"]
    shots = shots[["player", "team", "minute", "shot_statsbomb_xg", "shot_outcome"]]
    expected_goals_by_team = shots.groupby("team")["shot_statsbomb_xg"].sum()
    sorted_shots = shots.sort_values("shot_statsbomb_xg", ascending = False).head()
    return sorted_shots, expected_goals_by_team
def get_attacking_stats(events):
    events = events[events["type"].isin(["Shot", "Pass", "Carry", "Dribble"])]
    events = events[["player", "team", "type"]]
    events = events.groupby(["player", "team", "type"]).size().unstack(fill_value=0)
    events["total_attacking_stats"] = events.sum(axis=1)
    events = events.reset_index()
    sorted_events = events.sort_values('total_attacking_stats', ascending=False)
    return sorted_events
def get_xg_timeline(events):
    shots = events[events["type"] == "Shot"]
    shots = shots[["minute", "second", "team", "player", "shot_statsbomb_xg", "shot_outcome"]]
    shots["cumulative_xg"] = shots.groupby("team")["shot_statsbomb_xg"].cumsum()
    return shots
def get_shot_map_data(events, team):
    events = events[events['team'] == team]
    shots = events[events['type'] == 'Shot']
    shots['x'] = shots['location'].str[0]
    shots['y'] = shots['location'].str[1]
    shots = shots[['player', 'team', 'minute','x','y', 'shot_statsbomb_xg', 'shot_outcome']]
    return shots
def get_pass_combinations(events, team):
    events = events[events['team'] == team]
    passes = events[events['type'] == 'Pass']
    passes = passes[['team', 'player', 'pass_recipient']]
    pass_combinations = passes.value_counts()
    pass_combinations = pass_combinations.reset_index(name = 'pass_count')
    pass_combinations = pass_combinations.rename(columns={'player':'passer', 'pass_recipient':'recipient'})
    pass_combinations = pass_combinations.sort_values(['team', 'pass_count'], ascending=[True, False])
    pass_combinations = pass_combinations[pass_combinations["pass_count"] >= 5].copy()
    return pass_combinations
def get_pass_network_data(events, lineups, team):
    lineups = lineups[team]
    lineup_numbers = lineups[['player_name', 'jersey_number']]
    events_by_team = events[events['team'] == team]
    passes = events_by_team[events_by_team['type'] == 'Pass']
    passes = passes.dropna(subset = ['pass_recipient'])
    pass_network = passes[['team', 'player', 'location']]
    pass_network['x'] = pass_network['location'].str[0]
    pass_network['y'] = pass_network['location'].str[1]
    pass_network = pass_network[['team', 'player','x', 'y']]
    pass_network = pass_network.groupby(['team','player']).agg(avg_x = ('x', 'mean'), avg_y = ('y','mean'), total_passes = ('player', 'size')).reset_index()
    pass_network = pass_network.sort_values(['team', 'total_passes'], ascending = [True, False])
    pass_network = pd.merge(pass_network, lineup_numbers, how = 'left', left_on = 'player', right_on = 'player_name')
    pass_network = pass_network.drop(columns="player_name")
    return pass_network
def get_pass_edges(events, lineups , team):
    pass_network = get_pass_network_data(events,lineups, team)
    pass_combinations = get_pass_combinations(events, team)
    pass_edges = pd.merge(pass_combinations, pass_network, how = 'inner', left_on = 'passer', right_on = 'player')
    pass_edges = pass_edges.rename(columns={"avg_x": "passer_x","avg_y": "passer_y"})
    pass_edges = pd.merge(pass_edges, pass_network, how = 'inner', left_on = 'recipient', right_on = 'player')
    pass_edges = pass_edges.rename(columns={'avg_x':'recipient_x', 'avg_y':'recipient_y'})
    pass_edges = pass_edges[['passer', 'team', 'pass_count' ,'passer_x', 'passer_y', 'recipient', 'recipient_x', 'recipient_y', ]]
    return pass_edges