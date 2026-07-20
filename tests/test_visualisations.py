from src.visualisations import get_percentage_share
import pandas as pd
def test_get_percentage_share_when_both_0():
    team_stats = pd.DataFrame({'Shots':[0,0]}, index = ['team1', 'team2'])
    assert get_percentage_share('Shots', team_stats, 'team1', 'team2') == (50,50)
def test_get_percentage_share_when_one_0():
    team_stats = pd.DataFrame({'Shots':[5,0]}, index = ['team1','team2'])
    assert get_percentage_share('Shots', team_stats, 'team1', 'team2') == (100,0)
def test_get_percentage_share_normal():
    team_stats = pd.DataFrame({'Shots':[3,2]}, index = ['team1', 'team2'])
    assert get_percentage_share('Shots', team_stats, 'team1', 'team2') == (60,40)