"""
Main API class for interacting with the BALLDONTLIE API
"""

import requests
from typing import List, Dict, Any, Optional, Union
import time
from .models import Player, Team, Game, PlayerStats


class NBAAPIError(Exception):
    """Custom exception for NBA API errors"""
    pass


class NBAAPI:
    """
    Main class for interacting with the BALLDONTLIE NBA API
    """
    
    BASE_URL = "https://www.balldontlie.io/api/v1"
    
    def __init__(self, rate_limit_delay: float = 0.6):
        """
        Initialize the NBA API client
        
        Args:
            rate_limit_delay: Delay between requests to avoid rate limiting (seconds)
        """
        self.rate_limit_delay = rate_limit_delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'SimpleNBA-API/1.0.0'
        })
    
    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a request to the API with rate limiting
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            
        Returns:
            JSON response data
            
        Raises:
            NBAAPIError: If the request fails
        """
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            # Rate limiting
            time.sleep(self.rate_limit_delay)
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise NBAAPIError(f"API request failed: {e}")
        except ValueError as e:
            raise NBAAPIError(f"Invalid JSON response: {e}")
    
    def get_all_teams(self) -> List[Team]:
        """
        Get all NBA teams
        
        Returns:
            List of Team objects
        """
        data = self._make_request("teams")
        return [Team.from_dict(team) for team in data.get('data', [])]
    
    def get_team(self, team_id: int) -> Optional[Team]:
        """
        Get a specific team by ID
        
        Args:
            team_id: Team ID
            
        Returns:
            Team object or None if not found
        """
        try:
            data = self._make_request(f"teams/{team_id}")
            return Team.from_dict(data)
        except NBAAPIError:
            return None
    
    def search_players(self, search: Optional[str] = None, page: int = 1, 
                      per_page: int = 25) -> Dict[str, Any]:
        """
        Search for players
        
        Args:
            search: Player name to search for
            page: Page number
            per_page: Number of results per page
            
        Returns:
            Dictionary with players data and pagination info
        """
        params = {
            'page': page,
            'per_page': min(per_page, 100)  # API limit
        }
        
        if search:
            params['search'] = search
        
        data = self._make_request("players", params)
        
        players = [Player.from_dict(player) for player in data.get('data', [])]
        
        return {
            'players': players,
            'meta': data.get('meta', {}),
            'pagination': {
                'current_page': data.get('meta', {}).get('current_page', 1),
                'total_pages': data.get('meta', {}).get('total_pages', 1),
                'total_count': data.get('meta', {}).get('total_count', 0),
                'per_page': data.get('meta', {}).get('per_page', per_page)
            }
        }
    
    def get_player(self, player_id: int) -> Optional[Player]:
        """
        Get a specific player by ID
        
        Args:
            player_id: Player ID
            
        Returns:
            Player object or None if not found
        """
        try:
            data = self._make_request(f"players/{player_id}")
            return Player.from_dict(data)
        except NBAAPIError:
            return None
    
    def get_games(self, seasons: Optional[List[int]] = None, 
                  team_ids: Optional[List[int]] = None,
                  start_date: Optional[str] = None,
                  end_date: Optional[str] = None,
                  postseason: Optional[bool] = None,
                  page: int = 1, per_page: int = 25) -> Dict[str, Any]:
        """
        Get games with various filters
        
        Args:
            seasons: List of season years (e.g., [2023])
            team_ids: List of team IDs
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            postseason: Filter for postseason games
            page: Page number
            per_page: Number of results per page
            
        Returns:
            Dictionary with games data and pagination info
        """
        params = {
            'page': page,
            'per_page': min(per_page, 100)
        }
        
        if seasons:
            params['seasons[]'] = seasons
        if team_ids:
            params['team_ids[]'] = team_ids
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
        if postseason is not None:
            params['postseason'] = postseason
        
        data = self._make_request("games", params)
        
        games = [Game.from_dict(game) for game in data.get('data', [])]
        
        return {
            'games': games,
            'meta': data.get('meta', {}),
            'pagination': {
                'current_page': data.get('meta', {}).get('current_page', 1),
                'total_pages': data.get('meta', {}).get('total_pages', 1),
                'total_count': data.get('meta', {}).get('total_count', 0),
                'per_page': data.get('meta', {}).get('per_page', per_page)
            }
        }
    
    def get_game(self, game_id: int) -> Optional[Game]:
        """
        Get a specific game by ID
        
        Args:
            game_id: Game ID
            
        Returns:
            Game object or None if not found
        """
        try:
            data = self._make_request(f"games/{game_id}")
            return Game.from_dict(data)
        except NBAAPIError:
            return None
    
    def get_player_stats(self, seasons: Optional[List[int]] = None,
                        player_ids: Optional[List[int]] = None,
                        game_ids: Optional[List[int]] = None,
                        start_date: Optional[str] = None,
                        end_date: Optional[str] = None,
                        postseason: Optional[bool] = None,
                        page: int = 1, per_page: int = 25) -> Dict[str, Any]:
        """
        Get player statistics
        
        Args:
            seasons: List of season years
            player_ids: List of player IDs
            game_ids: List of game IDs
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            postseason: Filter for postseason stats
            page: Page number
            per_page: Number of results per page
            
        Returns:
            Dictionary with stats data and pagination info
        """
        params = {
            'page': page,
            'per_page': min(per_page, 100)
        }
        
        if seasons:
            params['seasons[]'] = seasons
        if player_ids:
            params['player_ids[]'] = player_ids
        if game_ids:
            params['game_ids[]'] = game_ids
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
        if postseason is not None:
            params['postseason'] = postseason
        
        data = self._make_request("stats", params)
        
        stats = [PlayerStats.from_dict(stat) for stat in data.get('data', [])]
        
        return {
            'stats': stats,
            'meta': data.get('meta', {}),
            'pagination': {
                'current_page': data.get('meta', {}).get('current_page', 1),
                'total_pages': data.get('meta', {}).get('total_pages', 1),
                'total_count': data.get('meta', {}).get('total_count', 0),
                'per_page': data.get('meta', {}).get('per_page', per_page)
            }
        }
    
    def get_season_averages(self, season: int, player_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get season averages for a player or all players
        
        Args:
            season: Season year
            player_id: Specific player ID (optional)
            
        Returns:
            List of season average statistics
        """
        params = {'season': season}
        if player_id:
            params['player_ids[]'] = [player_id]
        
        data = self._make_request("season_averages", params)
        return data.get('data', [])
    
    def find_player_by_name(self, first_name: str, last_name: str) -> Optional[Player]:
        """
        Find a player by their first and last name
        
        Args:
            first_name: Player's first name
            last_name: Player's last name
            
        Returns:
            Player object or None if not found
        """
        search_term = f"{first_name} {last_name}".strip()
        result = self.search_players(search=search_term, per_page=50)
        
        for player in result['players']:
            if (player.first_name.lower() == first_name.lower() and 
                player.last_name.lower() == last_name.lower()):
                return player
        
        return None
    
    def get_team_roster(self, team_id: int, season: Optional[int] = None) -> List[Player]:
        """
        Get all players for a specific team
        
        Args:
            team_id: Team ID
            season: Season year (optional)
            
        Returns:
            List of Player objects
        """
        all_players = []
        page = 1
        
        while True:
            result = self.search_players(page=page, per_page=100)
            team_players = [p for p in result['players'] if p.team and p.team.id == team_id]
            all_players.extend(team_players)
            
            if page >= result['pagination']['total_pages']:
                break
            page += 1
        
        return all_players