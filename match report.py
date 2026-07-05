import pandas as pd
from statsbombpy import sb
def match_report(match_id):
    lineups, events, team1, team2 = load_match_data(match_id)
    team1_goals, team2_goals = count_shot_outcome_by_team("Goal", events, team1, team2)
    team1_score, team2_score = get_score(events, team1, team2)
    team1_shots, team2_shots = count_events_by_team("Shot", events, team1, team2)
    team1_passes, team2_passes = count_events_by_team("Pass", events, team1, team2)
    team1_dribbles, team2_dribbles = count_events_by_team("Dribble", events, team1, team2)
    team1_carries, team2_carries = count_events_by_team("Carry", events, team1, team2)
    team1_pressures, team2_pressures = count_events_by_team("Pressure", events, team1, team2)
    team1_fouls, team2_fouls = count_events_by_team("Foul Committed", events, team1, team2)   
    team1_shots_off_target, team2_shots_off_target = count_shot_outcome_by_team("Off T", events, team1, team2)
    team1_shots_blocked, team2_shots_blocked = count_shot_outcome_by_team("Blocked", events, team1, team2)
    team1_shots_saved, team2_shots_saved = count_shot_outcome_by_team("Saved", events, team1, team2)
    team1_shots_on_target = team1_shots_saved + team1_goals
    team2_shots_on_target = team2_shots_saved + team2_goals
    top_players_by_events = get_top_players_by_events(events, 5)
    team_stats = pd.DataFrame([
        {
            "team":team1,
            "goals":team1_score,
            "shots":team1_shots,
            "passes":team1_passes,
            "dribbles":team1_dribbles,
            "carries":team1_carries,
            "pressures":team1_pressures,
            "fouls_committed":team1_fouls
            },
        {
            "team":team2,
            "goals":team2_score,
            "shots":team2_shots,
            "passes":team2_passes,
            "dribbles":team2_dribbles,
            "carries":team2_carries,
            "pressures":team2_pressures,
            "fouls_committed":team2_fouls
        },
    ])
    shot_summary = pd.DataFrame([
        {
            "team":team1,
            "total_shots":team1_shots,
            "goals":team1_score,
            "shots_on_target":team1_shots_on_target,
            "shots_blocked":team1_shots_blocked,
            "shots_off_target":team1_shots_off_target
        },
        {
            "team":team2,
            "total_shots":team2_shots,
            "goals":team2_score,
            "shots_on_target":team2_shots_on_target,
            "shots_blocked":team2_shots_blocked,
            "shots_off_target":team2_shots_off_target
        },
    ])
    return {
        "match_id":match_id,
        "teams":[team1, team2],
        "score":{
            team1:team1_score,
            team2:team2_score
        },
        "team_stats":team_stats,
        "shot_summary":shot_summary,
        "top_players":top_players_by_events,
    }
def get_score(events, team1, team2):
    team1_goals, team2_goals = count_shot_outcome_by_team("Goal", events, team1, team2)
    team1_own_goals_for, team2_own_goals_for = count_events_by_team("Own Goal For", events, team1, team2)
    return(team1_goals + team1_own_goals_for), (team2_goals + team2_own_goals_for)
def load_match_data(match_id):
    lineups = sb.lineups(match_id = match_id)
    events = sb.events(match_id = match_id)
    events = events.dropna(how = 'all', axis = 1)
    teams = list(lineups.keys())
    team1 = teams[0]
    team2 = teams[1]
    return lineups, events, team1, team2
def count_events_by_team(event, events, team1, team2):
    event_everyone = events[events["type"] == event]
    event_by_team = event_everyone["team"].value_counts()
    team1_count = event_by_team.get(team1, 0)
    team2_count = event_by_team.get(team2, 0)
    return team1_count, team2_count
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
def print_match_report(report):
    team1, team2 = report["teams"]
    score = report["score"]
    shots = report["team_stats"]["shots"]
    passes = report["team_stats"]["passes"]
    carries = report["team_stats"]["carries"]
    pressures = report["team_stats"]["pressures"]
    fouls_committed = report["team_stats"]["fouls_committed"]
    top_players = report["top_players"]
    shots_on_target = report["shot_summary"]["shots_on_target"]
    shots_off_target = report["shot_summary"]["shots_off_target"]
    shots_blocked = report["shot_summary"]["shots_blocked"]
    print(f"Match: {team1} {score[team1]}-{score[team2]} {team2}")
    print("\nBasic stats: ")
    print(f"{team1}:")
    print(f"- Shots: {shots.iloc[0]}")
    print(f"- Goals: {score[team1]}")
    print(f"- Passes: {passes.iloc[0]}")
    print(f"- Carries: {carries.iloc[0]}")
    print(f"- Pressures: {pressures.iloc[0]}")
    print(f"- Fouls Committed: {fouls_committed.iloc[0]}")
    print(f"\n{team2}:")
    print(f"- Shots: {shots.iloc[1]}")
    print(f"- Goals: {score[team2]}")
    print(f"- Passes: {passes.iloc[1]}")
    print(f"- Carries: {carries.iloc[1]}")
    print(f"- Pressures: {pressures.iloc[1]}")
    print(f"- Fouls Committed: {fouls_committed.iloc[1]}")
    print("\nTop players:")
    print(top_players.to_string(index=False))
    print(f"\nShot Summary:\n{team1}:")
    print(f"- Total Shots: {shots.iloc[0]}")
    print(f"- Goals: {score[team1]}")
    print(f"- Shots On Target: {shots_on_target.iloc[0]}")
    print(f"- Shots Off Target: {shots_off_target.iloc[0]}")
    print(f"- Shots Blocked: {shots_blocked.iloc[0]}")
    print(f"\n{team2}: ")
    print(f"- Total Shots: {shots.iloc[1]}")
    print(f"- Goals: {score[team2]}")
    print(f"- Shots On Target: {shots_on_target.iloc[1]}")
    print(f"- Shots Off Target: {shots_off_target.iloc[1]}")
    print(f"- Shots Blocked: {shots_blocked.iloc[1]}")
report = match_report(3749253)
print_match_report(report)
