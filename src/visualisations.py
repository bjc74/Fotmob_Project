import matplotlib.pyplot as plt
import os
import pandas as pd
from mplsoccer import Pitch

def plot_team_stats(report, output_dir):
    match_id = report["match_id"]
    os.makedirs(output_dir, exist_ok=True)
    normalised_stats_by_metric = normalise_stats_by_metric(report)
    normalised_stats_by_metric.plot.bar(rot = 45)
    plot_team_stats_path = os.path.join(output_dir, f"match_{match_id}_plot.png")
    plt.ylabel("Share of match total (%)")
    plt.title(f"Team event share by metric — match {match_id}")
    plt.tight_layout()
    plt.savefig(plot_team_stats_path)
    plt.show()
    plt.close()
def get_percentage_share(event_type, team_stats, team1, team2):
    if team_stats.loc[team1, event_type] == 0 and team_stats.loc[team2, event_type] == 0:
        return 50, 50
    else:
        team1_share = team_stats.loc[team1, event_type]/(team_stats.loc[team1, event_type] + team_stats.loc[team2, event_type]) *100
        return team1_share, 100 - team1_share
def normalise_stats_by_metric(report):
    team1,team2 = report["teams"]
    team_stats = report["team_stats"].set_index("team")
    team1_normalised_shots, team2_normalised_shots = get_percentage_share('shots', team_stats, team1, team2)
    team1_normalised_carries, team2_normalised_carries = get_percentage_share('carries', team_stats, team1,team2)
    team1_normalised_pressures, team2_normalised_pressures = get_percentage_share('pressures', team_stats, team1, team2)
    team1_normalised_passes, team2_normalised_passes = get_percentage_share('passes', team_stats, team1, team2)
    team1_normalised_fouls_committed, team2_normalised_fouls_committed = get_percentage_share('fouls_committed', team_stats, team1, team2)
    team1_normalised_xG, team2_normalised_xG = get_percentage_share('xG', team_stats, team1, team2)
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
        "normalised_xG":{
            team1:team1_normalised_xG,
            team2:team2_normalised_xG
        }
    })
    return pd.DataFrame(stats_by_metric).T
def plot_pass_network(match_id, report, team, output_dir):
    pitch = Pitch(pitch_type="statsbomb")
    fig, ax = pitch.draw()
    pass_network = report["pass_network"][team]
    pass_edges = report["pass_edges"][team]
    pass_network_data_path  = os.path.join(output_dir, f'match_{match_id}_{team}_pass_network.png')
    pitch.scatter(x = pass_network['avg_x'], y = pass_network['avg_y'], s = pass_network['total_passes']*10, ax = ax, zorder = 2)
    for _, row in pass_network.iterrows():
        if pd.notna(row['jersey_number']) and row['jersey_number'] != 0:
            label = int(row["jersey_number"])
        else:
            label = row["player"].split()[-1]
        ax.annotate(label,(row["avg_x"], row["avg_y"]),ha="center",va="center", zorder = 3)
    max_line_width = pass_edges['pass_count'].max()
    for _,row in pass_edges.iterrows():
        ax.plot((row['passer_x'] ,row['recipient_x']),(row['passer_y'], row['recipient_y']), lw = 0.5 + row['pass_count']*5/max_line_width, color = 'red', alpha = 0.4, zorder = 1)
    plt.title(f'{team} pass network - Match {match_id}')
    plt.ylabel('')
    plt.xlabel('')
    plt.tight_layout()
    plt.savefig(pass_network_data_path)
    plt.show()
    plt.close(fig)
def plot_shot_map(match_id, team, report, output_dir):
    pitch = Pitch(pitch_type="statsbomb", half = True)
    fig, ax = pitch.draw()
    shot_map_path = os.path.join(output_dir, f'match_{match_id}_{team}_shot_map.png')
    shot_map_data = report['shot_map_data'][team].copy()
    shot_map_data['point_sizes'] = shot_map_data['shot_statsbomb_xg']*500
    pitch.scatter(x = shot_map_data['x'], y = shot_map_data['y'], s = shot_map_data['point_sizes'], ax = ax, color = 'red', alpha = 0.6)
    goals = shot_map_data[shot_map_data['shot_outcome'] == 'Goal']
    pitch.scatter(x = goals['x'], y = goals['y'], s = goals['point_sizes'], label = 'Goal', marker = '*', ax = ax, color = 'gold', edgecolor = 'black')
    ax.legend(loc="upper left")
    plt.ylabel('')
    plt.xlabel('')
    plt.title(f'{team} shot Map - match {match_id}')
    plt.tight_layout()
    plt.savefig(shot_map_path)
    plt.show()
    plt.close(fig)
def plot_xG_race(match_id, report, output_dir):
    team1, team2 = report["teams"]
    xG_race = report['xG_timeline'].copy()
    xG_race['time'] = (xG_race['minute'] + (xG_race['second']/60))
    xG_race = xG_race[['time','team','cumulative_xG']]
    fig, ax = plt.subplots()
    for team in [team1, team2]:
        team_data = xG_race[xG_race["team"] == team]
        ax.step(team_data["time"],team_data["cumulative_xG"],where="post",label=team,)
    xG_race_path = os.path.join(output_dir, f'match_{match_id}_xG_race.png')
    ax.set_ylabel("Cumulative xG")
    ax.set_title(f"xG race - match {match_id}")
    ax.legend()
    plt.tight_layout()
    plt.savefig(xG_race_path)
    plt.show()
    plt.close(fig)
def plot_graphs(match_id, report, output_dir, team_stats = False, xG_race = False, shot_map = False, pass_network = False):
    os.makedirs(output_dir, exist_ok=True)
    team1, team2 = report['teams']
    if team_stats:
        plot_team_stats(report, output_dir)
    if xG_race:
        plot_xG_race(match_id, report, output_dir)
    if shot_map:
        plot_shot_map(match_id, team1, report, output_dir)
        plot_shot_map(match_id, team2, report, output_dir)
    if pass_network:
        plot_pass_network(match_id,report, team1, output_dir)
        plot_pass_network(match_id,report, team2, output_dir)