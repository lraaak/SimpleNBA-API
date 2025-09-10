"""
Utility functions for SimpleNBA-API
"""

from typing import List, Dict, Any, Optional
import json
import csv
from datetime import datetime, timedelta
from .models import Player, Team, Game, PlayerStats


def export_players_to_csv(players: List[Player], filename: str) -> None:
    """
    Export players list to CSV file
    
    Args:
        players: List of Player objects
        filename: Output filename
    """
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'first_name', 'last_name', 'position', 'height_feet', 
                     'height_inches', 'weight_pounds', 'team_name', 'team_abbreviation']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for player in players:
            writer.writerow({
                'id': player.id,
                'first_name': player.first_name,
                'last_name': player.last_name,
                'position': player.position,
                'height_feet': player.height_feet,
                'height_inches': player.height_inches,
                'weight_pounds': player.weight_pounds,
                'team_name': player.team.full_name if player.team else None,
                'team_abbreviation': player.team.abbreviation if player.team else None
            })


def export_games_to_csv(games: List[Game], filename: str) -> None:
    """
    Export games list to CSV file
    
    Args:
        games: List of Game objects
        filename: Output filename
    """
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'date', 'home_team', 'visitor_team', 'home_score', 
                     'visitor_score', 'winner', 'season', 'postseason']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for game in games:
            winner = None
            if game.winner:
                winner = game.winner.abbreviation
            
            writer.writerow({
                'id': game.id,
                'date': game.date,
                'home_team': game.home_team.abbreviation,
                'visitor_team': game.visitor_team.abbreviation,
                'home_score': game.home_team_score,
                'visitor_score': game.visitor_team_score,
                'winner': winner,
                'season': game.season,
                'postseason': game.postseason
            })


def export_stats_to_csv(stats: List[PlayerStats], filename: str) -> None:
    """
    Export player statistics to CSV file
    
    Args:
        stats: List of PlayerStats objects
        filename: Output filename
    """
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['player_name', 'team', 'game_date', 'opponent', 'min', 'pts', 
                     'reb', 'ast', 'stl', 'blk', 'fgm', 'fga', 'fg_pct', 'fg3m', 
                     'fg3a', 'fg3_pct', 'ftm', 'fta', 'ft_pct', 'turnover', 'pf']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for stat in stats:
            # Determine opponent
            if stat.team.id == stat.game.home_team.id:
                opponent = stat.game.visitor_team.abbreviation
            else:
                opponent = stat.game.home_team.abbreviation
            
            writer.writerow({
                'player_name': stat.player.full_name,
                'team': stat.team.abbreviation,
                'game_date': stat.game.date,
                'opponent': opponent,
                'min': stat.min,
                'pts': stat.pts,
                'reb': stat.reb,
                'ast': stat.ast,
                'stl': stat.stl,
                'blk': stat.blk,
                'fgm': stat.fgm,
                'fga': stat.fga,
                'fg_pct': stat.fg_percentage,
                'fg3m': stat.fg3m,
                'fg3a': stat.fg3a,
                'fg3_pct': stat.fg3_percentage,
                'ftm': stat.ftm,
                'fta': stat.fta,
                'ft_pct': stat.ft_percentage,
                'turnover': stat.turnover,
                'pf': stat.pf
            })


def calculate_team_record(games: List[Game], team: Team) -> Dict[str, int]:
    """
    Calculate team's win-loss record from games
    
    Args:
        games: List of games
        team: Team to analyze
        
    Returns:
        Dictionary with wins, losses, and total games
    """
    wins = 0
    losses = 0
    
    for game in games:
        if game.status == "Final":
            if game.winner and game.winner.id == team.id:
                wins += 1
            elif game.winner:  # Game finished but team didn't win
                losses += 1
    
    return {
        'wins': wins,
        'losses': losses,
        'games_played': wins + losses,
        'win_percentage': wins / (wins + losses) if (wins + losses) > 0 else 0
    }


def get_head_to_head_record(games: List[Game], team1: Team, team2: Team) -> Dict[str, Any]:
    """
    Get head-to-head record between two teams
    
    Args:
        games: List of games
        team1: First team
        team2: Second team
        
    Returns:
        Dictionary with head-to-head statistics
    """
    team1_wins = 0
    team2_wins = 0
    total_games = 0
    
    h2h_games = []
    
    for game in games:
        # Check if this game involves both teams
        teams_in_game = {game.home_team.id, game.visitor_team.id}
        if {team1.id, team2.id} == teams_in_game and game.status == "Final":
            total_games += 1
            h2h_games.append(game)
            
            if game.winner:
                if game.winner.id == team1.id:
                    team1_wins += 1
                elif game.winner.id == team2.id:
                    team2_wins += 1
    
    return {
        f'{team1.abbreviation}_wins': team1_wins,
        f'{team2.abbreviation}_wins': team2_wins,
        'total_games': total_games,
        'games': h2h_games
    }


def get_player_averages(stats: List[PlayerStats]) -> Dict[str, float]:
    """
    Calculate player averages from statistics
    
    Args:
        stats: List of PlayerStats objects
        
    Returns:
        Dictionary with averaged statistics
    """
    if not stats:
        return {}
    
    totals = {
        'games': len(stats),
        'pts': 0, 'reb': 0, 'ast': 0, 'stl': 0, 'blk': 0,
        'fgm': 0, 'fga': 0, 'fg3m': 0, 'fg3a': 0,
        'ftm': 0, 'fta': 0, 'turnover': 0, 'pf': 0
    }
    
    for stat in stats:
        for key in totals:
            if key != 'games' and hasattr(stat, key):
                value = getattr(stat, key)
                if value is not None:
                    totals[key] += value
    
    games_played = totals['games']
    averages = {}
    
    for key, total in totals.items():
        if key == 'games':
            averages[key] = total
        else:
            averages[key] = round(total / games_played, 1) if games_played > 0 else 0
    
    # Calculate percentages
    if totals['fga'] > 0:
        averages['fg_pct'] = round(totals['fgm'] / totals['fga'], 3)
    if totals['fg3a'] > 0:
        averages['fg3_pct'] = round(totals['fg3m'] / totals['fg3a'], 3)
    if totals['fta'] > 0:
        averages['ft_pct'] = round(totals['ftm'] / totals['fta'], 3)
    
    return averages


def format_stat_line(stats: PlayerStats) -> str:
    """
    Format a player's stat line as a readable string
    
    Args:
        stats: PlayerStats object
        
    Returns:
        Formatted stat line string
    """
    pts = stats.pts or 0
    reb = stats.reb or 0
    ast = stats.ast or 0
    
    stat_line = f"{pts} PTS, {reb} REB, {ast} AST"
    
    if stats.stl:
        stat_line += f", {stats.stl} STL"
    if stats.blk:
        stat_line += f", {stats.blk} BLK"
    
    # Add shooting percentages if available
    if stats.fg_percentage:
        stat_line += f" | FG: {stats.fg_percentage}%"
    if stats.fg3_percentage:
        stat_line += f", 3P: {stats.fg3_percentage}%"
    if stats.ft_percentage:
        stat_line += f", FT: {stats.ft_percentage}%"
    
    return stat_line


def get_season_dates(season: int) -> Dict[str, str]:
    """
    Get approximate start and end dates for an NBA season
    
    Args:
        season: Season year (e.g., 2023 for 2023-24 season)
        
    Returns:
        Dictionary with start_date and end_date
    """
    # NBA seasons typically start in October and end in April of the following year
    start_date = f"{season}-10-01"
    end_date = f"{season + 1}-04-30"
    
    return {
        'start_date': start_date,
        'end_date': end_date
    }


def search_players_fuzzy(players: List[Player], query: str, limit: int = 10) -> List[Player]:
    """
    Fuzzy search for players by name
    
    Args:
        players: List of Player objects to search
        query: Search query
        limit: Maximum number of results
        
    Returns:
        List of matching players
    """
    query = query.lower().strip()
    if not query:
        return players[:limit]
    
    # Exact matches first
    exact_matches = []
    partial_matches = []
    
    for player in players:
        full_name = player.full_name.lower()
        first_name = player.first_name.lower()
        last_name = player.last_name.lower()
        
        if query == full_name or query == first_name or query == last_name:
            exact_matches.append(player)
        elif (query in full_name or query in first_name or query in last_name or
              full_name.startswith(query) or last_name.startswith(query)):
            partial_matches.append(player)
    
    # Return exact matches first, then partial matches
    results = exact_matches + partial_matches
    return results[:limit]