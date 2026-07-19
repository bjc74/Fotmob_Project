import pandas as pd
from src.analytics import get_score, count_shot_outcome_by_team, count_events_by_team
def test_get_score():
    events = pd.DataFrame({'type':['Shot', 'Shot', 'Shot'],
                          'shot_outcome':['Goal' ,'Goal', 'Goal'], 
                          'team':['team1', 'team1', 'team2']})
    assert get_score(events, 'team1', 'team2') == (2,1)
def test_get_score_when_own_goals():
    events = pd.DataFrame({'type':['Shot', 'Shot', 'Shot', 'Own Goal For'],
                          'shot_outcome':['Goal' ,'Goal', 'Goal', 'NaN'], 
                          'team':['team1', 'team1', 'team2', 'team1']})
    assert get_score(events, 'team1', 'team2') == (3,1)