# Fotmob_Project
# Mini FotMob / Football Match Report Generator

This project uses StatsBomb open event data to generate a basic football match report for a given match ID.

The report includes:
- Final score
- Team-level event counts
- Shots, passes, carries, dribbles, pressures and fouls committed
- Shot summary by team
- Shots on target, off target and blocked shots
- Top players by event count
- Handling of own goals in the score calculation

## Why I built this

I built this project to practise Python, Pandas, football event data analysis, and basic project structure using real sports data.

The aim is to turn raw football event data into readable team and player reports, similar to a simplified FotMob-style match summary.

## How it works

The main workflow is:

```python
report = match_report(match_id)
print_match_report(report)
```
## Example report
Match: Liverpool 1-2 Arsenal

Basic stats: 
Liverpool:
- Shots: 14
- Goals: 1
- Passes: 490
- Carries: 308
- Pressures: 127
- Fouls Committed: 13

Arsenal:
- Shots: 12
- Goals: 2
- Passes: 461
- Carries: 379
- Pressures: 137
- Fouls Committed: 20

Top players:
                  player  events
El-Hadji Ousseynou Diouf     211
            Harry Kewell     210
          Steven Gerrard     207
            Robert Pirès     204
             Ray Parlour     196

Shot Summary:
Liverpool:
- Total Shots: 14
- Goals: 1
- Shots On Target: 4
- Shots Off Target: 6
- Shots Blocked: 3

Arsenal: 
- Total Shots: 12
- Goals: 2
- Shots On Target: 6
- Shots Off Target: 4
- Shots Blocked: 1