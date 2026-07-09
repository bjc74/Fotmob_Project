import sqlite3 
import pandas as pd
con  = sqlite3.connect(":memory:")
def run_query(query):
    return pd.read_sql_query(query, con)
df1 = pd.read_csv("outputs/match_3749493_team_stats.csv")
df2= pd.read_csv("outputs/match_3749493_shot_summary.csv")
df3 = pd.read_csv("outputs/match_3749493_top_players.csv")
df4 = pd.read_csv("outputs/match_3749493_top_xg_shots.csv")
df5 = pd.read_csv("outputs/match_3749493_top_on_ball_contributors.csv")
df1.to_sql(name = "team_stats", con = con, index = False, if_exists='replace')
df2.to_sql(name = "shot_summary", con = con, index = False, if_exists='replace')
df3.to_sql(name = "top_players", con = con, index = False, if_exists='replace')
df4.to_sql(name = "top_xg_shots", con = con, index = False, if_exists='replace')
df5.to_sql(name = "top_on_ball_contributors", con = con, index = False, if_exists='replace')
query1 = '''
SELECT team_stats.team, team_stats.goals, team_stats.xg, team_stats.shots, shots_on_target, shots_off_target, shots_blocked, passes, dribbles, carries, pressures, fouls_committed
FROM team_stats
INNER JOIN shot_summary ON team_stats.team = shot_summary.team
ORDER BY team_stats.xg DESC;
'''
query2 = '''
SELECT team, goals, total_shots, shots_on_target, shots_on_target *100 / CAST(total_shots AS FLOAT) AS Shot_accuracy, goals/CAST(total_shots AS FLOAT) AS goals_per_shot, goals/CAST(shots_on_target AS FLOAT) as goals_per_shot_on_target
FROM shot_summary
ORDER BY goals_per_shot DESC;
'''
query3 = '''
SELECT team, goals, xg, goals - xg AS xg_overperformance, CAST(goals AS FLOAT)/xg AS goals_per_xg
FROM team_stats
ORDER BY xg_overperformance DESC;
'''
query4 = '''
SELECT team, passes, carries, pressures, passes + carries AS pass_carry_total, CAST(pressures AS FLOAT)/passes AS pressure_to_pass_ratio
FROM team_stats
ORDER BY pass_carry_total DESC; 
'''
query5 = '''
SELECT player, top_xg_shots.team, minute, shot_outcome, shot_statsbomb_xg, goals AS team_goals, xg AS team_xg
FROM top_xg_shots
INNER JOIN team_stats ON top_xg_shots.team  = team_stats.team
ORDER BY shot_statsbomb_xg DESC LIMIT 5;
'''
query6 = '''
SELECT player, top_on_ball_contributors.team, Shot, Pass, Carry, Dribble, total_attacking_stats AS total_on_ball_contributions, xg AS team_xg, goals AS team_goals
FROM top_on_ball_contributors
INNER JOIN team_stats ON top_on_ball_contributors.team = team_stats.team
ORDER BY total_on_ball_contributions DESC LIMIT 10;
'''
query7 = '''
SELECT player, team, Shot, Pass, Carry, Dribble, CAST(Shot AS FLOAT)/SUM(Shot) OVER() AS shot_share, CAST(Pass AS FLOAT)/SUM(Pass) OVER() AS pass_share, CAST(Carry AS FLOAT)/SUM(Carry) OVER() AS carry_share, CAST(Dribble AS FLOAT)/SUM(Dribble) OVER() AS dribble_share, (CAST(Shot AS FLOAT)/SUM(Shot) OVER() + CAST(Pass AS FLOAT)/SUM(Pass) OVER() + CAST(Carry AS FLOAT)/SUM(Carry) OVER() + CAST(Dribble AS FLOAT)/SUM(Dribble) OVER()) AS balanced_score
FROM top_on_ball_contributors
ORDER BY balanced_score DESC LIMIT 10;
'''
query8 = '''
WITH temp AS(
SELECT team, goals, xg, row_number() OVER (ORDER BY team) AS rn
FROM team_stats)
SELECT team1.team AS team1, team2.team AS team2, team1.goals AS team1_goals, team2.goals AS team2_goals, team1.xg AS team1_xg, team2.xg AS team2_xg,
CASE
    WHEN team1.xg > team2.xg THEN team1.team
    WHEN team2.xg > team1.xg THEN team2.team
    ELSE 'Draw'
END AS xg_winner,
CASE
    WHEN team1.goals > team2.goals THEN team1.team
    WHEN team2.goals > team1.goals THEN team2.team
    ELSE 'Draw'
END AS actual_winner
FROM temp AS team1
JOIN temp AS team2
WHERE team1.rn = 1 AND team2.rn = 2
'''
queries = {
    "combined_team_report": query1,
    "shooting_efficiency": query2,
    "xg_finishing": query3,
    "possession_style": query4,
    "top_xg_shots": query5,
    "top_on_ball_players": query6,
    "balanced_player_score": query7,
    "match_summary": query8,
}
for name, query in queries.items():
    print(f"\n--- {name} ---")
    print(run_query(query))
import os

os.makedirs("outputs/sql_analysis", exist_ok=True)

for name, query in queries.items():
    result = run_query(query)
    result.to_csv(f"outputs/sql_analysis/{name}.csv", index=False)
