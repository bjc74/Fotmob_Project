# Football Match Analytics Report Generator

A Python football analytics project that transforms StatsBomb Open Data into match reports, CSV datasets, SQL analysis and football visualisations.

The program accepts a StatsBomb match ID through the command line, analyses the event data and saves all generated outputs in a match-specific folder.

## Features

### Match analysis

- Final-score calculation, including own goals
- Official-score validation
- Team event statistics
- Shot and expected-goals analysis
- Player involvement rankings
- Player attacking-contribution analysis

### Visualisations

- Expected-goals race
- Shot maps
- Pass networks
- Team event-share comparison

Pass networks include only completed passes with a recorded recipient.

### Data outputs

- Team statistics
- Shot summaries
- Player statistics
- Pass-network nodes
- Pass-network edges
- SQL analysis tables

### SQL analysis

- Shooting efficiency
- xG finishing performance
- Possession-style metrics
- Player attacking contribution
- Match-level goals and xG comparisons

### Testing

The project includes automated tests for core analytics behaviour, including:

- Normal scores, own goals and goalless matches
- Team event counting
- Player involvement rankings
- Completed-pass filtering
- Pass-combination aggregation
- Expected-goals calculations
- Percentage-share calculations

## Why I built this

I built this project to develop practical experience with Python, Pandas, SQL, testing, data visualisation and modular software design using real football event data.

The project converts raw StatsBomb events into readable match reports and visual analytics resembling the information available on football analytics platforms.

## Example visualisations

### Expected-goals race

![Expected-goals race](docs/images/xG_race.png)

### Shot map

![Shot map](docs/images/shot_map.png)

### Pass network

![Pass network](docs/images/pass_network.png)

### Normalised statistics by team

![Normalised statistics by team](docs/images/normalised_stats_by_team.png)

## Installation

Clone the repository:

```bash
git clone https://github.com/bjc74/Fotmob_Project.git
cd Fotmob_Project
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Running the project

Run the program from the repository root and provide a StatsBomb Open Data match ID:

```bash
python src/main.py --match-id 3749493
```

The program:

1. Loads the match events and line-ups.
2. Generates the match report.
3. Calculates team, player, shot and xG statistics.
4. Validates the calculated score against the official result.
5. Exports tabular outputs as CSV files.
6. Generates the selected visualisations as PNG files.

Outputs are saved in a match-specific folder:

```text
outputs/match_3749493/
```

Using a different match ID creates a separate output folder.

If the supplied match ID is unavailable through StatsBomb Open Data, the program displays an explanatory error message rather than continuing with incomplete data.

## Example report

```text
Match: Everton 1-2 Arsenal

Basic stats:
Everton:
- Shots: 15
- Goals: 1
- xG: 1.27
- Passes: 381
- Carries: 235
- Pressures: 271
- Fouls Committed: 19

Arsenal:
- Shots: 14
- Goals: 2
- xG: 2.12
- Passes: 422
- Carries: 342
- Pressures: 117
- Fouls Committed: 11

Top players:
                     player  events
            Thomas Gravesen     248
             Patrick Vieira     230
Gilberto Aparecido da Silva     178
              Thierry Henry     178
 Laureano Bisan-Etame Mayer     165

Top xG shots:
          player    team  minute  shot_statsbomb_xg shot_outcome
   Thierry Henry Arsenal      34            0.783500         Goal
   Nick Chadwick Everton       6            0.421668        Saved
  Patrick Vieira Arsenal      57            0.378841        Saved
    Robert Pirès Arsenal      57            0.319439         Goal
Tomasz Radziński Everton      83            0.200138         Goal

Top players by attacking statistics:
                     player    team  Carry  Dribble  Pass  Shot  total_attacking_stats
             Patrick Vieira Arsenal     52        5    62     3                    122
            Thomas Gravesen Everton     50        3    58     2                    113
 Laureano Bisan-Etame Mayer Arsenal     42        2    52     0                     96
         Alessandro Pistone Everton     33        1    55     0                     89
               Robert Pirès Arsenal     40        6    39     3                     88
Gilberto Aparecido da Silva Arsenal     39        0    49     0                     88
          Fredrik Ljungberg Arsenal     38        5    39     1                     83
              Thierry Henry Arsenal     35        7    29     4                     75
                Ashley Cole Arsenal     26        3    37     0                     66
             David Unsworth Everton     21        0    39     0                     60

Shot summary:
Everton:
- Total Shots: 15
- xG: 1.27
- Goals: 1
- Shots On Target: 5
- Shots Off Target: 5
- Shots Blocked: 5

Arsenal:
- Total Shots: 14
- xG: 2.12
- Goals: 2
- Shots On Target: 4
- Shots Off Target: 6
- Shots Blocked: 3
```

## Running the tests

Run the full test suite from the repository root:

```bash
python -m pytest
```

The tests use small, deterministic Pandas DataFrames rather than external API requests, making them fast and reproducible.

## Running the SQL analysis

After generating the required CSV outputs, run:

```bash
python src/sql_analysis.py
```

The SQL outputs are saved under:

```text
outputs/sql_analysis/
```

They include shooting-efficiency, xG-finishing, possession-style, player-contribution and match-summary tables.

## Project structure

```text
Fotmob_Project/
├── docs/
│   └── images/
│       ├── normalised_stats_by_team.png
│       ├── pass_network.png
│       ├── shot_map.png
│       └── xG_race.png
├── src/
│   ├── __init__.py
│   ├── analytics.py
│   ├── main.py
│   ├── match_report.py
│   ├── sql_analysis.py
│   └── visualisations.py
├── tests/
│   ├── test_analytics.py
│   └── test_visualisations.py
├── .gitattributes
├── .gitignore
├── README.md
└── requirements.txt
```

Generated files under `outputs/` are excluded from version control.

## Current limitations

- The project analyses one match at a time.
- The SQL analysis relies on previously exported CSV files.
- Some SQL inputs currently use fixed filenames.
- Analysis is limited to competitions available through StatsBomb Open Data.
- The project does not provide an interactive user interface.

## Possible future improvements

- Generalise the SQL pipeline for arbitrary match IDs.
- Support analysis across multiple matches and competitions.
- Add comparative team and player analysis.
- Build an interactive dashboard.
- Add continuous integration to run the tests automatically.

## Data source

Match event data is provided through StatsBomb Open Data.