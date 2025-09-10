"""
Unit tests for SimpleNBA-API
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add the parent directory to the path so we can import simplenba
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simplenba.api import NBAAPI, NBAAPIError
from simplenba.models import Player, Team, Game, PlayerStats
from simplenba.utils import calculate_team_record, get_player_averages


class TestModels(unittest.TestCase):
    """Test data models"""
    
    def test_team_creation(self):
        """Test Team model creation"""
        team_data = {
            'id': 1,
            'abbreviation': 'LAL',
            'city': 'Los Angeles',
            'conference': 'West',
            'division': 'Pacific',
            'full_name': 'Los Angeles Lakers',
            'name': 'Lakers'
        }
        
        team = Team.from_dict(team_data)
        
        self.assertEqual(team.id, 1)
        self.assertEqual(team.abbreviation, 'LAL')
        self.assertEqual(team.city, 'Los Angeles')
        self.assertEqual(str(team), 'Los Angeles Lakers (LAL)')
    
    def test_player_creation(self):
        """Test Player model creation"""
        team_data = {
            'id': 1,
            'abbreviation': 'LAL',
            'city': 'Los Angeles',
            'conference': 'West',
            'division': 'Pacific',
            'full_name': 'Los Angeles Lakers',
            'name': 'Lakers'
        }
        
        player_data = {
            'id': 123,
            'first_name': 'LeBron',
            'last_name': 'James',
            'position': 'F',
            'height_feet': 6,
            'height_inches': 9,
            'weight_pounds': 250,
            'team': team_data
        }
        
        player = Player.from_dict(player_data)
        
        self.assertEqual(player.id, 123)
        self.assertEqual(player.full_name, 'LeBron James')
        self.assertEqual(player.height_formatted, '6\'9"')
        self.assertEqual(player.team.abbreviation, 'LAL')
    
    def test_game_creation(self):
        """Test Game model creation"""
        team1_data = {
            'id': 1,
            'abbreviation': 'LAL',
            'city': 'Los Angeles',
            'conference': 'West',
            'division': 'Pacific',
            'full_name': 'Los Angeles Lakers',
            'name': 'Lakers'
        }
        
        team2_data = {
            'id': 2,
            'abbreviation': 'GSW',
            'city': 'Golden State',
            'conference': 'West',
            'division': 'Pacific',
            'full_name': 'Golden State Warriors',
            'name': 'Warriors'
        }
        
        game_data = {
            'id': 456,
            'date': '2023-01-15',
            'home_team': team1_data,
            'visitor_team': team2_data,
            'home_team_score': 110,
            'visitor_team_score': 105,
            'period': 4,
            'postseason': False,
            'season': 2023,
            'status': 'Final',
            'time': None
        }
        
        game = Game.from_dict(game_data)
        
        self.assertEqual(game.id, 456)
        self.assertEqual(game.home_team_score, 110)
        self.assertEqual(game.visitor_team_score, 105)
        self.assertEqual(game.winner.abbreviation, 'LAL')
        self.assertEqual(str(game), 'GSW @ LAL (2023-01-15)')


class TestAPI(unittest.TestCase):
    """Test NBA API functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.api = NBAAPI(rate_limit_delay=0)  # No delay for tests
    
    @patch('simplenba.api.requests.Session.get')
    def test_get_all_teams(self, mock_get):
        """Test getting all teams"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'data': [
                {
                    'id': 1,
                    'abbreviation': 'LAL',
                    'city': 'Los Angeles',
                    'conference': 'West',
                    'division': 'Pacific',
                    'full_name': 'Los Angeles Lakers',
                    'name': 'Lakers'
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        teams = self.api.get_all_teams()
        
        self.assertEqual(len(teams), 1)
        self.assertEqual(teams[0].abbreviation, 'LAL')
        self.assertEqual(teams[0].full_name, 'Los Angeles Lakers')
    
    @patch('simplenba.api.requests.Session.get')
    def test_search_players(self, mock_get):
        """Test player search"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'data': [
                {
                    'id': 123,
                    'first_name': 'LeBron',
                    'last_name': 'James',
                    'position': 'F',
                    'height_feet': 6,
                    'height_inches': 9,
                    'weight_pounds': 250,
                    'team': {
                        'id': 1,
                        'abbreviation': 'LAL',
                        'city': 'Los Angeles',
                        'conference': 'West',
                        'division': 'Pacific',
                        'full_name': 'Los Angeles Lakers',
                        'name': 'Lakers'
                    }
                }
            ],
            'meta': {
                'current_page': 1,
                'total_pages': 1,
                'total_count': 1,
                'per_page': 25
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = self.api.search_players(search='LeBron')
        
        self.assertEqual(len(result['players']), 1)
        self.assertEqual(result['players'][0].full_name, 'LeBron James')
        self.assertEqual(result['pagination']['total_count'], 1)
    
    @patch('requests.Session.get')
    def test_api_error_handling(self, mock_get):
        """Test API error handling"""
        import requests
        mock_get.side_effect = requests.exceptions.ConnectionError("Network error")
        
        with self.assertRaises(NBAAPIError):
            self.api.get_all_teams()


class TestUtils(unittest.TestCase):
    """Test utility functions"""
    
    def test_calculate_team_record(self):
        """Test team record calculation"""
        team = Team(id=1, abbreviation='LAL', city='Los Angeles', 
                   conference='West', division='Pacific', 
                   full_name='Los Angeles Lakers', name='Lakers')
        
        other_team = Team(id=2, abbreviation='GSW', city='Golden State',
                         conference='West', division='Pacific',
                         full_name='Golden State Warriors', name='Warriors')
        
        # Create games where LAL wins 2 and loses 1
        games = [
            Game(id=1, date='2023-01-01', home_team=team, visitor_team=other_team,
                 home_team_score=110, visitor_team_score=105, period=4,
                 postseason=False, season=2023, status='Final', time=None),
            Game(id=2, date='2023-01-02', home_team=other_team, visitor_team=team,
                 home_team_score=100, visitor_team_score=115, period=4,
                 postseason=False, season=2023, status='Final', time=None),
            Game(id=3, date='2023-01-03', home_team=team, visitor_team=other_team,
                 home_team_score=95, visitor_team_score=105, period=4,
                 postseason=False, season=2023, status='Final', time=None)
        ]
        
        record = calculate_team_record(games, team)
        
        self.assertEqual(record['wins'], 2)
        self.assertEqual(record['losses'], 1)
        self.assertEqual(record['games_played'], 3)
        self.assertAlmostEqual(record['win_percentage'], 0.667, places=2)
    
    def test_get_player_averages(self):
        """Test player averages calculation"""
        # Create mock player stats
        team = Team(id=1, abbreviation='LAL', city='Los Angeles',
                   conference='West', division='Pacific',
                   full_name='Los Angeles Lakers', name='Lakers')
        
        player = Player(id=123, first_name='LeBron', last_name='James',
                       position='F', height_feet=6, height_inches=9,
                       weight_pounds=250, team=team)
        
        game = Game(id=1, date='2023-01-01', home_team=team, visitor_team=team,
                   home_team_score=110, visitor_team_score=105, period=4,
                   postseason=False, season=2023, status='Final', time=None)
        
        stats = [
            PlayerStats(id=1, player=player, game=game, team=team, min='36:00',
                       fgm=10, fga=20, fg3m=3, fg3a=8, ftm=7, fta=8,
                       oreb=2, dreb=8, reb=10, ast=8, stl=2, blk=1,
                       turnover=4, pf=2, pts=30),
            PlayerStats(id=2, player=player, game=game, team=team, min='35:00',
                       fgm=8, fga=18, fg3m=2, fg3a=6, ftm=6, fta=7,
                       oreb=1, dreb=9, reb=10, ast=6, stl=1, blk=2,
                       turnover=3, pf=3, pts=24)
        ]
        
        averages = get_player_averages(stats)
        
        self.assertEqual(averages['games'], 2)
        self.assertEqual(averages['pts'], 27.0)  # (30 + 24) / 2
        self.assertEqual(averages['reb'], 10.0)  # (10 + 10) / 2
        self.assertEqual(averages['ast'], 7.0)   # (8 + 6) / 2


if __name__ == '__main__':
    unittest.main()