import pandas as pd
from statsbombpy import sb
import matplotlib.pyplot as plt
import os

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
def export_report(report, output_dir="outputs"):
    os.makedirs(output_dir, exist_ok=True)
    match_id = report["match_id"]
    team_stats_path = os.path.join(output_dir, f"match_{match_id}_team_stats.csv")
    shot_summary_path = os.path.join(output_dir, f"match_{match_id}_shot_summary.csv")
    top_players_path = os.path.join (output_dir, f"match_{match_id}_top_players.csv")
    team_stats_csv = report["team_stats"].to_csv(team_stats_path, index = False)
    shot_summary_csv = report["shot_summary"].to_csv(shot_summary_path, index = False)
    top_players_csv = report["top_players"].to_csv(top_players_path, index = False)
def validate_scores(competition_id, season_id, n=20):
    matches = sb.matches(competition_id=competition_id, season_id=season_id)
    errors = []
    for i in range(n):
        match_id = matches["match_id"].iloc[i]
        home_score_offical = matches["home_score"].iloc[i]
        away_score_official = matches["away_score"].iloc[i]
        home_team = matches["home_team"].iloc[i]
        away_team = matches["away_team"].iloc[i]
        report = match_report(match_id)
        score = report["score"]
        home_score_calculated = score.get(home_team)
        away_score_calculated = score.get(away_team)
        if home_score_offical != home_score_calculated and away_score_official != away_score_calculated:
            errors.append({
                "match_id":match_id,
                "home_team":home_team,
                "away_team":away_team,
                "home_score_official":home_score_offical,
                "home_score_calculated":home_score_calculated,
                "away_score_official":away_score_official,
                "away_score_calculated":away_score_calculated
            })
    return pd.DataFrame(errors)
def match_report_from_competition(competition_id, season_id, match_id):
    matches = sb.matches(competition_id=competition_id, season_id=season_id)
    match = matches[matches["match_id"] == match_id].iloc[0]
    home_team = match["home_team"]
    away_team = match["away_team"]
    return match_report(match_id, home_team=home_team, away_team=away_team)
def plot_team_stats(report, output_dir="outputs"):
    match_id = report["match_id"]
    os.makedirs(output_dir, exist_ok=True)
    team1, team2 = report["teams"]
    normalised_stats_by_metric = normalise_stats_by_metric(report)
    normalised_stats_by_metric.plot.bar(rot = 45)
    plot_team_stats_path = os.path.join(output_dir, f"match_{match_id}_plot.png")
    plt.ylabel("Share of match total (%)")
    plt.title(f"Team event share by metric — match {match_id}")
    plt.tight_layout()
    plt.savefig(plot_team_stats_path)
    plt.show()
    return normalised_stats_by_metric
def normalise_stats_by_metric(report):
    team1,team2 = report["teams"]
    shots = report["team_stats"]["shots"]
    carries = report["team_stats"]["carries"]
    pressures = report["team_stats"]["pressures"]
    passes = report["team_stats"]["passes"]
    fouls_committed = report["team_stats"]["fouls_committed"]
    team1_normalised_shots = shots.iloc[0]/(shots.iloc[0] + shots.iloc[1]) *100
    team2_normalised_shots = 100 - team1_normalised_shots
    team1_normalised_carries = carries.iloc[0]/(carries.iloc[0]+carries.iloc[1]) *100
    team2_normalised_carries = 100 - team1_normalised_carries
    team1_normalised_pressures = pressures.iloc[0]/(pressures.iloc[0]+pressures.iloc[1])*100
    team2_normalised_pressures = 100 - team1_normalised_pressures
    team1_normalised_passes = passes.iloc[0]/(passes.iloc[0]+passes.iloc[1])*100
    team2_normalised_passes = 100 - team1_normalised_passes
    team1_normalised_fouls_committed = fouls_committed.iloc[0]/(fouls_committed.iloc[0]+fouls_committed.iloc[1])*100
    team2_normalised_fouls_committed = 100 - team1_normalised_fouls_committed
    stats_by_metric = ({
        "normalised_shots":{
            team1:team1_normalised_shots,
            team2:team2_normalised_shots
        },
        "normalised_passes":{
            team1:team1_normalised_passes,
            team2:team2_normalised_passes
        },
        "normalised_carries":{
            team1:team1_normalised_carries,
            team2:team2_normalised_carries
        },
        "normalised_pressures":{
            team1:team1_normalised_pressures,
            team2:team2_normalised_pressures
        },
        "normalised_fouls_committed":{
            team1:team1_normalised_fouls_committed,
            team2:team2_normalised_fouls_committed
        }
    })
    return pd.DataFrame(stats_by_metric).T
report = match_report(3749493)
print_match_report(report)
export_report(report, output_dir="outputs")
print(validate_scores(2, 44))
plot_team_stats(report)