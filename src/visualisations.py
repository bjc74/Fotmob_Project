import matplotlib.pyplot as plt
import os
import pandas as pd
from mplsoccer import Pitch

def plot_team_stats(report, output_dir="outputs"):
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
def plot_pass_network(match_id, report, team, output_dir = 'outputs'):
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
    plt.title(f'match_{match_id}_{team}_pass_network')
    plt.ylabel('')
    plt.xlabel('')
    plt.tight_layout()
    plt.savefig(pass_network_data_path)
    plt.show()
def plot_shot_map(match_id, team, report, output_dir = 'outputs'):
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
    plt.title(f'Shot Map {team} - match {match_id}')
    plt.tight_layout()
    plt.savefig(shot_map_path)
    plt.show()
def plot_xg_race(match_id, report, output_dir = 'outputs'):
    team1, team2 = report["teams"]
    xg_race = report['xg_timeline'].copy()
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
    plt.show()
def plot_graphs(match_id, report, output_dir = 'outputs', team_stats = False, xg_race = False, shot_map = False, pass_network = False):
    team1, team2 = report['teams']
    if team_stats == True:
        plot_team_stats(report, output_dir)
    if xg_race == True:
        plot_xg_race(match_id, report, output_dir)
    if shot_map == True:
        plot_shot_map(match_id, team1, report, output_dir)
        plot_shot_map(match_id, team2, report, output_dir)
    if pass_network == True:
        plot_pass_network(match_id,report, team1, output_dir)
        plot_pass_network(match_id,report, team2, output_dir)