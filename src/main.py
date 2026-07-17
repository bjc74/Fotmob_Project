from match_report import match_report, export_report
from visualisations import plot_graphs

match_id = 3749493
report = match_report(match_id)

export_report(report)

plot_graphs(
    match_id,
    report,
    team_stats=True,
    xg_race=True,
    shot_map=True,
    pass_network=True,
)