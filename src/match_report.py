import pandas as pd
from statsbombpy import sb
import os
from analytics import load_match_data, get_score, count_events_by_team, get_top_players_by_events, count_shot_outcome_by_team, get_xg_stats, get_attacking_stats, get_xg_timeline, get_shot_map_data, get_pass_network_data, get_pass_edges
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
    top_on_ball_contributors = get_attacking_stats(events)
    top_xg_shots, xg_by_team = get_xg_stats(events)
    xg_timeline = get_xg_timeline(events)
    shot_map_data_team1 = get_shot_map_data(events, team1)
    shot_map_data_team2 = get_shot_map_data(events, team2)
    pass_network_team1 = get_pass_network_data(events, lineups, team1)
    pass_network_team2 = get_pass_network_data(events, lineups, team2)
    pass_edges_team1 = get_pass_edges(events, lineups, team1)
    pass_edges_team2 = get_pass_edges(events, lineups, team2)
    team1_xg = xg_by_team.loc[team1]
    team2_xg = xg_by_team.loc[team2]
    team_stats = pd.DataFrame([
        {
            "team":team1,
            "goals":team1_score,
            "shots":team1_shots,
            "xg":team1_xg,
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
            "xg":team2_xg,
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
            "xg":team1_xg,
            "goals":team1_score,
            "shots_on_target":team1_shots_on_target,
            "shots_blocked":team1_shots_blocked,
            "shots_off_target":team1_shots_off_target
        },
        {
            "team":team2,
            "total_shots":team2_shots,
            "xg":team2_xg,
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
        "top_xg_shots":top_xg_shots,
        "top_on_ball_contributors":top_on_ball_contributors,
        "xg_timeline":xg_timeline,
        "shot_map_data":{
            team1:shot_map_data_team1,
            team2:shot_map_data_team2
        },
        'pass_network':{team1: pass_network_team1,
                        team2 : pass_network_team2
        },
        'pass_edges':{
            team1:pass_edges_team1,
            team2:pass_edges_team2
        }
                        
    }
def print_match_report(report):
    team_stats = report["team_stats"].set_index("team")
    shot_summary = report["shot_summary"].set_index("team")
    team1, team2 = report["teams"]
    score = report["score"]
    top_players = report["top_players"]
    top_xg_shots = report["top_xg_shots"]
    top_on_ball_contributors = report["top_on_ball_contributors"].head(10)
    print(f"Match: {team1} {score[team1]}-{score[team2]} {team2}")
    print("\nBasic stats: ")
    print(f"{team1}:")
    print(f"- Shots: {team_stats.loc[team1, "shots"]}")
    print(f"- Goals: {score[team1]}")
    print(f"- XG: {team_stats.loc[team1,"xg"]:.2f}")
    print(f"- Passes: {team_stats.loc[team1, "passes"]}")
    print(f"- Carries: {team_stats.loc[team1, "carries"]}")
    print(f"- Pressures: {team_stats.loc[team1, "pressures"]}")
    print(f"- Fouls Committed: {team_stats.loc[team1, "fouls_committed"]}")
    print(f"\n{team2}:")
    print(f"- Shots: {team_stats.loc[team2, "shots"]}")
    print(f"- Goals: {score[team2]}")
    print(f"- XG: {team_stats.loc[team2, "xg"]:.2f}")
    print(f"- Passes: {team_stats.loc[team2, "passes"]}")
    print(f"- Carries: {team_stats.loc[team2, "carries"]}")
    print(f"- Pressures: {team_stats.loc[team2, "pressures"]}")
    print(f"- Fouls Committed: {team_stats.loc[team2, "fouls_committed"]}")
    print("\nTop players:")
    print(top_players.to_string(index=False))
    print("\nTop XG shots:")
    print(top_xg_shots.to_string(index = False))
    print("\nTop Players by attacking stats:")
    print(top_on_ball_contributors.to_string(index = False))
    print(f"\nShot Summary:\n{team1}:")
    print(f"- Total Shots: {shot_summary.loc[team1, "total_shots"]}")
    print(f"- XG: {shot_summary.loc[team1, "xg"]:.2f}")
    print(f"- Goals: {score[team1]}")
    print(f"- Shots On Target: {shot_summary.loc[team1, "shots_on_target"]}")
    print(f"- Shots Off Target: {shot_summary.loc[team1, "shots_off_target"]}")
    print(f"- Shots Blocked: {shot_summary.loc[team1, "shots_blocked"]}")
    print(f"\n{team2}: ")
    print(f"- Total Shots: {shot_summary.loc[team2, "total_shots"]}")
    print(f"- XG: {shot_summary.loc[team2, "xg"]:.2f}")
    print(f"- Goals: {score[team2]}")
    print(f"- Shots On Target: {shot_summary.loc[team2, "shots_on_target"]}")
    print(f"- Shots Off Target: {shot_summary.loc[team2, "shots_off_target"]}")
    print(f"- Shots Blocked: {shot_summary.loc[team2, "shots_blocked"]}")
def export_report(report, output_dir="outputs"):
    os.makedirs(output_dir, exist_ok=True)
    match_id = report["match_id"]
    team1, team2 = report['teams']
    team_stats_path = os.path.join(output_dir, f"match_{match_id}_team_stats.csv")
    shot_summary_path = os.path.join(output_dir, f"match_{match_id}_shot_summary.csv")
    top_players_path = os.path.join (output_dir, f"match_{match_id}_top_players.csv")
    top_xg_shots_path = os.path.join(output_dir, f"match_{match_id}_top_xg_shots.csv")
    top_on_ball_contributors_path = os.path.join(output_dir, f"match_{match_id}_top_on_ball_contributors.csv")
    xg_timeline_path = os.path.join(output_dir, f"match_{match_id}_xg_timeline.csv")
    shot_map_data_team1_path = os.path.join(output_dir, f"match_{match_id}_{team1}_shot_map_data.csv")
    shot_map_data_team2_path = os.path.join(output_dir, f"match_{match_id}_{team2}_shot_map_data.csv")
    pass_network_team1_path = os.path.join(output_dir, f'match_{match_id}_{team1}_pass_network.csv')
    pass_network_team2_path = os.path.join(output_dir, f'match_{match_id}_{team2}_pass_network.csv')
    pass_edges_team1_path = os.path.join(output_dir, f'match_{match_id}_{team1}_pass_edges.csv')
    pass_edges_team2_path = os.path.join(output_dir, f'match_{match_id}_{team2}_pass_edges.csv')
    team_stats_csv = report["team_stats"].to_csv(team_stats_path, index = False)
    shot_summary_csv = report["shot_summary"].to_csv(shot_summary_path, index = False)
    top_players_csv = report["top_players"].to_csv(top_players_path, index = False)
    top_xg_shots_csv = report["top_xg_shots"].to_csv(top_xg_shots_path, index = False)
    top_on_ball_contributors_csv = report["top_on_ball_contributors"].to_csv(top_on_ball_contributors_path, index = False)
    xg_timeline_csv = report["xg_timeline"].to_csv(xg_timeline_path, index = False)
    shot_map_data_team1_csv = report['shot_map_data'][team1].to_csv(shot_map_data_team1_path, index = False)
    shot_map_data_team2_csv = report['shot_map_data'][team2].to_csv(shot_map_data_team2_path, index = False)
    pass_network_team1_csv = report['pass_network'][team1].to_csv(pass_network_team1_path, index = False)
    pass_network_team2_csv = report['pass_network'][team2].to_csv(pass_network_team2_path, index = False)
    pass_edges_team1_csv = report['pass_edges'][team1].to_csv(pass_edges_team1_path, index = False)
    pass_edges_team2_csv = report['pass_edges'][team2].to_csv(pass_edges_team2_path, index = False)
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
        if home_score_offical != home_score_calculated or away_score_official != away_score_calculated:
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




