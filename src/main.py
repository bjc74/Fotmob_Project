from match_report import export_report, match_report, print_match_report
from visualisations import plot_graphs


def main():
    match_id = 3749493

    report = match_report(match_id)

    print_match_report(report)
    export_report(report)

    plot_graphs(
        match_id,
        report,
        team_stats=True,
        xG_race=True,
        shot_map=True,
        pass_network=True,
    )


if __name__ == "__main__":
    main()