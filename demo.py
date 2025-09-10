#!/usr/bin/env python3
"""
Demo script for SimpleNBA-API
Shows example usage without requiring actual API calls
"""

from simplenba.models import Team, Player, Game
from simplenba.utils import calculate_team_record, format_stat_line
import json

def demo_models():
    """Demonstrate data models"""
    print("🏀 SimpleNBA-API Demo")
    print("=" * 50)
    
    # Create sample team
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
    print(f"Team: {team}")
    
    # Create sample player
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
    print(f"Player: {player.full_name}")
    print(f"Height: {player.height_formatted}")
    print(f"Team: {player.team.abbreviation}")
    
    # Create sample game
    opponent_data = {
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
        'home_team': team_data,
        'visitor_team': opponent_data,
        'home_team_score': 110,
        'visitor_team_score': 105,
        'period': 4,
        'postseason': False,
        'season': 2023,
        'status': 'Final',
        'time': None
    }
    game = Game.from_dict(game_data)
    print(f"\nGame: {game}")
    print(f"Winner: {game.winner.abbreviation}")
    
    return team, player, game

def demo_utils():
    """Demonstrate utility functions"""
    print("\n📊 Utility Functions Demo")
    print("=" * 50)
    
    # Demo team record calculation
    team = Team(id=1, abbreviation='LAL', city='Los Angeles',
               conference='West', division='Pacific',
               full_name='Los Angeles Lakers', name='Lakers')
    
    other_team = Team(id=2, abbreviation='GSW', city='Golden State',
                     conference='West', division='Pacific',
                     full_name='Golden State Warriors', name='Warriors')
    
    # Create sample games (2 wins, 1 loss for LAL)
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
    print(f"Team Record: {record['wins']}-{record['losses']}")
    print(f"Win Percentage: {record['win_percentage']:.1%}")

def demo_cli_usage():
    """Show CLI usage examples"""
    print("\n💻 CLI Usage Examples")
    print("=" * 50)
    
    cli_examples = [
        "# Search for players",
        "nba-cli players --search 'LeBron James'",
        "",
        "# List all teams",
        "nba-cli teams",
        "",
        "# Filter teams by conference",
        "nba-cli teams --conference West",
        "",
        "# Search for games",
        "nba-cli games --season 2023 --team LAL",
        "",
        "# Get player information",
        "nba-cli player-info LeBron James --season 2023",
        "",
        "# Get team roster",
        "nba-cli roster LAL"
    ]
    
    for example in cli_examples:
        print(example)

def demo_web_features():
    """Show web interface features"""
    print("\n🌐 Web Interface Features")
    print("=" * 50)
    
    features = [
        "✅ Beautiful, responsive design with Bootstrap",
        "✅ Advanced player search with pagination",
        "✅ Team browsing by conference and division",
        "✅ Game filtering by season, team, and date",
        "✅ Detailed player profiles with statistics",
        "✅ Team rosters and recent games",
        "✅ Mobile-friendly interface",
        "✅ Real-time data from BALLDONTLIE API"
    ]
    
    for feature in features:
        print(feature)
    
    print("\nTo start the web server:")
    print("python -m simplenba.webapp")
    print("Then visit: http://localhost:5000")

def demo_python_api():
    """Show Python API usage"""
    print("\n🐍 Python API Usage")
    print("=" * 50)
    
    code_example = '''
from simplenba import NBAAPI

# Initialize the API client
api = NBAAPI()

# Search for players
result = api.search_players(search="LeBron James")
players = result['players']

# Get all teams
teams = api.get_all_teams()

# Get games for a specific season
games = api.get_games(seasons=[2023], per_page=10)

# Get player statistics
stats = api.get_player_stats(seasons=[2023], per_page=20)

# Export data to CSV
from simplenba.utils import export_players_to_csv
export_players_to_csv(players, 'players.csv')
'''
    
    print(code_example)

if __name__ == "__main__":
    demo_models()
    demo_utils()
    demo_cli_usage()
    demo_web_features()
    demo_python_api()
    
    print("\n🎉 Demo Complete!")
    print("This NBA API provides comprehensive access to:")
    print("• Player data and statistics")
    print("• Team information and rosters")
    print("• Game results and history")
    print("• Data visualization capabilities")
    print("• Both CLI and web interfaces")
    print("\nFor more information, check the README.md file!")