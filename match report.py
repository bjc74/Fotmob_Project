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
    top_on_ball_contributors = get_attacking_stats(match_id=match_id)
    top_xg_shots, xg_by_team = get_xg_stats(match_id)
    xg_timeline = get_xg_timeline(match_id=match_id)
    shot_map_data = get_shot_map_data(match_id=match_id)
    pass_combinations= get_pass_combinations(match_id)
    pass_network = get_pass_network_data(match_id)
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
        "shot_map_data":shot_map_data,
        "pass_combinations":pass_combinations,
        'pass_network':pass_network
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
    team_stats_path = os.path.join(output_dir, f"match_{match_id}_team_stats.csv")
    shot_summary_path = os.path.join(output_dir, f"match_{match_id}_shot_summary.csv")
    top_players_path = os.path.join (output_dir, f"match_{match_id}_top_players.csv")
    top_xg_shots_path = os.path.join(output_dir, f"match_{match_id}_top_xg_shots.csv")
    top_on_ball_contributors_path = os.path.join(output_dir, f"match_{match_id}_top_on_ball_contributors.csv")
    xg_timeline_path = os.path.join(output_dir, f"match_{match_id}_xg_timeline.csv")
    shot_map_data_path = os.path.join(output_dir, f"match_{match_id}_shot_map_data.csv")
    pass_combinations_path = os.path.join(output_dir, f'match_{match_id}_pass_combinations.csv')
    pass_network_path = os.path.join(output_dir, f'match_{match_id}_pass_network.csv')
    team_stats_csv = report["team_stats"].to_csv(team_stats_path, index = False)
    shot_summary_csv = report["shot_summary"].to_csv(shot_summary_path, index = False)
    top_players_csv = report["top_players"].to_csv(top_players_path, index = False)
    top_xg_shots_csv = report["top_xg_shots"].to_csv(top_xg_shots_path, index = False)
    top_on_ball_contributors_csv = report["top_on_ball_contributors"].to_csv(top_on_ball_contributors_path, index = False)
    xg_timeline_csv = report["xg_timeline"].to_csv(xg_timeline_path, index = False)
    shot_map_data_csv = report['shot_map_data'].to_csv(shot_map_data_path, index = False)
    pass_combinations_csv = report['pass_combinations'].to_csv(pass_combinations_path, index = False)
    pass_network_csv = report['pass_network'].to_csv(pass_network_path, index = False)
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
    xg_race = report['xg_timeline']
    xg_race['time'] = (xg_race['minute'] + (xg_race['second']/60))
    xg_race = xg_race[['time','team','cumulative_xg']]
    ax = xg_race[xg_race['team'] == team1].plot.line(x = 'time', y = 'cumulative_xg', rot = 0, label = team1)
    xg_race[xg_race['team'] == team2].plot.line(x = 'time', y = 'cumulative_xg', rot = 0, ax = ax, label = team2)
    xg_race_path = os.path.join(output_dir, f'match_{match_id}_xg_race.png')
    plt.ylabel("Cumulative XG")
    plt.title(f"Xg race between teams - match {match_id}")
    plt.legend()
    plt.tight_layout()
    plt.savefig(xg_race_path)
    shot_map_path = os.path.join(output_dir, f'match_{match_id}_shot_map.png')
    shot_map_data = report['shot_map_data']
    shot_map_data['point_sizes'] = shot_map_data['shot_statsbomb_xg']*500
    ax = shot_map_data[shot_map_data['team'] == team1].plot.scatter(x = 'x', y = 'y', s = 'point_sizes', label = team1, color = 'red')
    shot_map_data[shot_map_data['team'] == team2].plot.scatter(x = 'x', y = 'y',s = 'point_sizes', label = team2, ax = ax, color = 'blue')
    shot_map_data[shot_map_data['shot_outcome'] == 'Goal'].plot.scatter(x = 'x', y = 'y',s = 'point_sizes', label = 'Goal', ax = ax, marker = '*', color = 'green')
    plt.ylabel('y location')
    plt.xlabel('x location')
    plt.title(f'Shot Map - match {match_id}')
    plt.legend()
    plt.tight_layout()
    plt.savefig(shot_map_path)
    pass_network_data_path  =os.path.join(output_dir, f'match_{match_id}_pass_network.png')
    pass_network_data = report['pass_network']
    ax1 = pass_network_data.plot.scatter(x = 'avg_x_passed', y = 'avg_y_passed', s = 'total_passes')
    for _, row in pass_network_data.iterrows():
        ax1.annotate(row["player"],(row["avg_x_passed"], row["avg_y_passed"]),fontsize=8)
    plt.legend()
    plt.show()
def normalise_stats_by_metric(report):
    team1,team2 = report["teams"]
    team_stats = report["team_stats"].set_index("team")
    team1_normalised_shots = team_stats.loc[team1, "shots"] /(team_stats.loc[team1, "shots"] + team_stats.loc[team2, "shots"]) *100
    team2_normalised_shots = 100 - team1_normalised_shots
    team1_normalised_carries = team_stats.loc[team1, "carries"]/(team_stats.loc[team1, "carries"] + team_stats.loc[team2, "carries"])*100
    team2_normalised_carries = 100 - team1_normalised_carries
    team1_normalised_pressures = team_stats.loc[team1, "pressures"]/(team_stats.loc[team1, "pressures"] + team_stats.loc[team2, "pressures"])*100
    team2_normalised_pressures = 100 - team1_normalised_pressures
    team1_normalised_passes = team_stats.loc[team1, "passes"]/(team_stats.loc[team1, "passes"] + team_stats.loc[team2, "passes"])*100
    team2_normalised_passes = 100 - team1_normalised_passes
    team1_normalised_fouls_committed = team_stats.loc[team1, "fouls_committed"]/(team_stats.loc[team1, "fouls_committed"]+team_stats.loc[team2, "fouls_committed"])*100
    team2_normalised_fouls_committed = 100 - team1_normalised_fouls_committed
    team1_normalised_xg = team_stats.loc[team1, "xg"]/(team_stats.loc[team1, "xg"] + team_stats.loc[team2, "xg"])*100
    team2_normalised_xg = 100 - team1_normalised_xg
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
        },
        "normalised_xg":{
            team1:team1_normalised_xg,
            team2:team2_normalised_xg
        }
    })
    return pd.DataFrame(stats_by_metric).T
def get_xg_stats(match_id):
    events = sb.events(match_id=match_id)
    shots = events[events["type"] == "Shot"]
    shots = shots[["player", "team", "minute", "shot_statsbomb_xg", "shot_outcome"]]
    expected_goals_by_team = shots.groupby("team")["shot_statsbomb_xg"].sum()
    sorted_shots = shots.sort_values("shot_statsbomb_xg", ascending = False).head()
    return sorted_shots, expected_goals_by_team
def get_attacking_stats(match_id):
    events = sb.events(match_id=match_id)
    events = events[events["type"].isin(["Shot", "Pass", "Carry", "Dribble"])]
    events = events[["player", "team", "type"]]
    events = events.groupby(["player", "team", "type"]).size().unstack(fill_value=0)
    events["total_attacking_stats"] = events.sum(axis=1)
    events = events.reset_index()
    sorted_events = events.sort_values('total_attacking_stats', ascending=False)
    return sorted_events
def get_xg_timeline(match_id):
    events = sb.events(match_id = match_id)
    shots = events[events["type"] == "Shot"]
    shots = shots[["minute", "second", "team", "player", "shot_statsbomb_xg", "shot_outcome"]]
    shots["cumulative_xg"] = shots.groupby("team")["shot_statsbomb_xg"].cumsum()
    return shots
def get_shot_map_data(match_id):
    events = sb.events(match_id=match_id)
    shots = events[events['type'] == 'Shot']
    shots['x'] = shots['location'].str[0]
    shots['y'] = shots['location'].str[1]
    shots = shots[['player', 'team', 'minute','x','y', 'shot_statsbomb_xg', 'shot_outcome']]
    return shots
def get_pass_combinations(match_id):
    events = sb.events(match_id)
    passes = events[events['type'] == 'Pass']
    passes = passes[['team', 'player', 'pass_recipient']]
    pass_combinations = passes.value_counts()
    pass_combinations = pass_combinations.reset_index(name = 'pass_count')
    pass_combinations = pass_combinations.rename(columns={'player':'passer', 'pass_recipient':'recipient'})
    pass_combinations = pass_combinations.sort_values(['team', 'pass_count'], ascending=[True, False])
    return pass_combinations
def get_pass_network_data(match_id):
    events = sb.events(match_id)
    passes = events[events['type'] == 'Pass']
    pass_network = passes[['team', 'player', 'location', 'pass_end_location']]
    pass_network['x_passed'] = pass_network['location'].str[0]
    pass_network['y_passed'] = pass_network['location'].str[1]
    pass_network['x_recieved'] = pass_network['pass_end_location'].str[0]
    pass_network['y_recieved'] = pass_network['pass_end_location'].str[1]
    pass_network = pass_network[['team', 'player','x_passed', 'y_passed', 'x_recieved', 'y_recieved']]
    pass_network = pass_network.groupby(['team','player']).agg(avg_x_passed = ('x_passed', 'mean'), avg_y_passed = ('y_passed','mean'), avg_x_recieved = ('x_recieved','mean'), avg_y_recieved = ('y_recieved', 'mean'), total_passes = ('player', 'size')).reset_index()
    return pass_network
report = match_report(3749493)
#print_match_report(report)
export_report(report, output_dir="outputs")
#validate_scores(2, 44)
plot_team_stats(report)
get_pass_network_data(3749493)


