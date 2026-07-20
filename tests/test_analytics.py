import pandas as pd
import pytest
from src.analytics import get_score, count_events_by_team, get_top_players_by_events, filter_completed_passes, get_pass_combinations, get_xG_stats
def test_get_score():
    events = pd.DataFrame({'type':['Shot', 'Shot', 'Shot'],
                          'shot_outcome':['Goal' ,'Goal', 'Goal'], 
                          'team':['team1', 'team1', 'team2']})
    assert get_score(events, 'team1', 'team2') == (2,1)
def test_get_score_when_own_goals():
    events = pd.DataFrame({'type':['Shot', 'Shot', 'Shot', 'Own Goal For'],
                          'shot_outcome':['Goal' ,'Goal', 'Goal', pd.NA], 
                          'team':['team1', 'team1', 'team2', 'team1']})
    assert get_score(events, 'team1', 'team2') == (3,1)
def test_get_score_when_0_0():
    events = pd.DataFrame({'type':['Shot', 'Pass', 'Carry', 'Dribble'],
                           'shot_outcome':['Saved', pd.NA, pd.NA , pd.NA],
                           'team':['team1', 'team1', 'team1', 'team2']

    })
    assert get_score(events, 'team1', 'team2') == (0,0)
def test_count_events_by_team_normal():
    events = pd.DataFrame({'type':['Shot','Shot', 'Shot', 'Shot', 'Own Goal For', 'Pass', 'Dribble', 'Pass', 'Carry', 'Dribble','Dribble'],
                           'team':['team1', 'team1', 'team2', 'team1','team1', 'team1', 'team2', 'team1', 'team1', 'team2', 'team1']
                           })
    assert count_events_by_team('Dribble', events, 'team1', 'team2') == (1,2)
def test_count_events_by_team_when_both_0():
    events = pd.DataFrame({'type':['Shot','Shot', 'Shot', 'Shot', 'Own Goal For', 'Pass', 'Dribble', 'Pass', 'Carry', 'Dribble'],
                           'team':['team1', 'team1', 'team2', 'team1','team1', 'team1', 'team2', 'team1', 'team1', 'team2']
                           })
    assert count_events_by_team('Tackle', events, 'team1', 'team2') == (0,0)
def test_count_events_by_team_when_one_0():
    events = pd.DataFrame({'type':['Shot','Shot', 'Shot', 'Shot', 'Own Goal For', 'Pass', 'Dribble', 'Pass', 'Carry', 'Dribble', 'Tackle'],
                           'team':['team1', 'team1', 'team2', 'team1','team1', 'team1', 'team2', 'team1', 'team1', 'team2', 'team1']
                           })
    assert count_events_by_team('Tackle', events, 'team1', 'team2') == (1,0)
def test_get_top_players_by_events():
    events = pd.DataFrame({'type':['Shot','Shot', 'Shot', 'Shot', 'Own Goal For', 'Pass', 'Dribble', 'Pass', 'Carry', 'Dribble', 'Pass','Shot','Shot', 'Shot', 'Shot', 'Own Goal For', 'Pass', 'Dribble', 'Pass', 'Carry', 'Dribble'],
                           'player':['player1', 'player2', 'player3', 'player4','player5', 'player6', 'player1', 'player2', 'player3', 'player4', 'player5', 'player1', 'player2', 'player3', 'player4', 'player1', 'player2', 'player3' ,'player1', 'player2', 'player1']
                           })
    assert get_top_players_by_events(events, 5)['player'].tolist() ==  ['player1', 'player2', 'player3', 'player4', 'player5']
    assert get_top_players_by_events(events,5)['events'].tolist() == [6,5,4,3,2]
def test_get_top_players_by_events_when_fewer_than_n():
    events = pd.DataFrame({'type':['Shot','Shot', 'Shot', 'Shot', 'Own Goal For', 'Pass', 'Dribble', 'Pass', 'Carry', 'Dribble', 'Pass','Shot','Shot', 'Shot', 'Shot', 'Own Goal For', 'Pass', 'Dribble', 'Pass', 'Carry', 'Dribble'],
                           'player':['player1', 'player2', 'player3', 'player4','player5', 'player6', 'player1', 'player2', 'player3', 'player4', 'player5', 'player1', 'player2', 'player3', 'player4', 'player1', 'player2', 'player3' ,'player1', 'player2', 'player1']
                           })
    assert get_top_players_by_events(events, 10)['player'].tolist() ==  ['player1', 'player2', 'player3', 'player4', 'player5','player6']
    assert get_top_players_by_events(events,10)['events'].tolist() == [6,5,4,3,2,1]
def test_filter_completed_passes():
    events = pd.DataFrame({'type':['Pass','Pass','Pass','pass','Pass','Pass','Pass','Shot','Pass','Pass','Pass','Shot'],
                           'pass_outcome':[pd.NA, pd.NA, 'Incomplete', pd.NA, pd.NA, 'Incomplete', pd.NA, pd.NA, 'Incomplete', pd.NA, pd.NA, 'incomplete'],
                           'pass_recipient':['player1', 'player2', pd.NA, 'player3', 'player4', pd.NA, 'player5', 'player6', pd.NA, 'player7', pd.NA, pd.NA],
                            'team':['team1','team1', 'team1','team1', 'team1','team1', 'team2', 'team2','team2', 'team2','team2', 'team2']
    })
    results = filter_completed_passes(events, 'team1')
    assert len(results) == 3
    assert results['pass_recipient'].tolist() == ['player1', 'player2', 'player4']
def test_filter_completed_passes_when_none():
    events = pd.DataFrame({'type':['pass', 'Pass', 'Shot', 'Pass', 'Pass'],
                           'pass_outcome':[pd.NA, 'Incomplete', pd.NA, 'Incomplete', pd.NA],
                           'pass_recipient':['player1', pd.NA, pd.NA, pd.NA, pd.NA],
                           'team':['team1', 'team1', 'team1', 'team2', 'team2']
    })
    result = filter_completed_passes(events, 'team1')
    assert result.empty
def test_get_pass_combinations():
    events = pd.DataFrame({'team':['team1','team1','team1','team1','team1','team1','team1','team1','team2', 'team2', 'team2', 'team2', 'team2', 'team2'],
                           'type':['Pass','Pass', 'Pass','pass','Shot', 'Pass','Pass', 'Pass','Pass','Dribble', 'Pass','Pass', 'Pass','Pass'],
                            'pass_outcome':[pd.NA, pd.NA, 'Incomplete', pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA],
                            'player':['player1', 'player2', 'player1', 'player1', 'player1', 'player2', 'player2', 'player2', 'player3', 'player3', 'player3', 'player3', 'player4', 'player4'],
                            'pass_recipient':[pd.NA, 'playerA', 'playerB', 'playerC', 'playerD', 'playerA', 'playerA', 'playerA', 'playerD', 'playerA', 'playerB', 'playerC', 'playerD', pd.NA]
    })
    result = get_pass_combinations(events, 'team1')
    assert result['passer'].tolist() == ['player2']
    assert result['recipient'].tolist() == ['playerA']
    assert result['pass_count'].tolist() == [4]
def test_get_xG_stats():
    events = pd.DataFrame({'type': ['Shot', 'Shot', 'Shot', 'Shot', 'Shot', 'Shot'],
                           'team':['team1', 'team2', 'team1','team2', 'team1', 'team2'],
                           'shot_statsbomb_xg':[0.78, 0.16, 0.12, 0.35, 0.32, 0.64],
                           'player':['player1', 'player2', 'player3', 'player4', 'player5', 'player6'],
                           'minute':[10, 22, 37, 55, 68, 89],
                           'shot_outcome':['Goal', 'Blocked', 'OffT', 'Saved', 'Saved', 'Goal']
                           })
    sorted_shots, expected_goals_by_team = get_xG_stats(events)
    sorted_shots = sorted_shots.reset_index(drop = True)
    assert sorted_shots.iloc[0]['minute'] == 10
    assert sorted_shots.iloc[0]['player'] == 'player1'
    assert sorted_shots.iloc[0]['shot_statsbomb_xg'] == pytest.approx(0.78)
    assert expected_goals_by_team['team1'] == pytest.approx(1.22)