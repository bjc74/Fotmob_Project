from match_report import export_report, match_report, print_match_report
from visualisations import plot_graphs
import argparse
import os
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--match-id", type=int, required=True)
    args = parser.parse_args()

    match_id = args.match_id
    try:
        report = match_report(match_id)
    except Exception:
        print(f'Could not load match {match_id}. Check that it exists in Statsbomb open data')
        return
    output_dir = f"outputs/match_{match_id}"
    os.makedirs(output_dir, exist_ok=True)

    export_report(report, output_dir=output_dir)
    print_match_report(report)

    plot_graphs(
        match_id,
        report,
        output_dir=output_dir,
        team_stats=True,
        xG_race=True,
        shot_map=True,
        pass_network=True,
    )


if __name__ == "__main__":
    main()