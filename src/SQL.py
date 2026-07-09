import sqlite3
import pandas as pd
def run_query(query):
    return pd.read_sql_query(query, con)
df = pd.read_csv("outputs/match_3749493_team_stats.csv")
df2 = pd.read_csv("outputs/match_3749493_shot_summary.csv")
df3 = pd.read_csv("outputs/match_3749493_top_xg_shots.csv")
df4 = pd.read_csv("outputs/match_3749493_top_on_ball_contributors.csv")
con = sqlite3.connect(":memory:")
df.to_sql(name = "team_stats", con=con, index = False, if_exists='replace')
df2.to_sql(name = "shot_summary", con = con, index = False, if_exists='replace')
df3.to_sql(name = "top_xg_shots", con = con, index = False, if_exists = 'replace')
df4.to_sql(name = "top_on_ball_contributors", con = con, index  =False, if_exists='replace')
query1 = '''
SELECT team, goals, shots, xg
FROM team_stats
ORDER BY xg DESC;
'''
query2 = '''
SELECT team, total_shots, shots_on_target, shots_off_target, shots_blocked
FROM shot_summary
ORDER BY total_shots DESC;
'''
query3 = '''
SELECT team, goals, total_shots, goals/CAST(total_shots AS FLOAT) AS goals_per_shot
FROM shot_summary
ORDER BY goals_per_shot DESC;
'''
query4 = '''
SELECT team, goals, xg, goals - xg AS xg_overperformance
FROM team_stats
ORDER BY xg_overperformance DESC;
'''
query5 = '''
SELECT player, team, minute, shot_outcome, shot_statsbomb_xg
FROM top_xg_shots
ORDER BY shot_statsbomb_xg DESC LIMIT 5;
'''
query6 = '''
SELECT player, team, shot, pass, carry, dribble, total_attacking_stats
FROM top_on_ball_contributors
ORDER BY total_attacking_stats DESC LIMIT 10;
'''
print(run_query(query1))
print(run_query(query2))
print(run_query(query3))
print(run_query(query4))
print(run_query(query5))
print(run_query(query6))