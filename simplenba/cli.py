"""
Command-line interface for SimpleNBA-API
"""

import click
from tabulate import tabulate
from colorama import init, Fore, Style
import sys
from typing import List, Optional

from .api import NBAAPI, NBAAPIError
from .models import Player, Team, Game, PlayerStats

# Initialize colorama for cross-platform colored output
init()


def success_print(message: str):
    """Print success message in green"""
    click.echo(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")


def error_print(message: str):
    """Print error message in red"""
    click.echo(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")


def info_print(message: str):
    """Print info message in blue"""
    click.echo(f"{Fore.BLUE}ℹ {message}{Style.RESET_ALL}")


def warning_print(message: str):
    """Print warning message in yellow"""
    click.echo(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")


def format_player_table(players: List[Player]) -> str:
    """Format players data as a table"""
    if not players:
        return "No players found."
    
    headers = ["ID", "Name", "Position", "Height", "Weight", "Team"]
    rows = []
    
    for player in players:
        team_name = player.team.abbreviation if player.team else "N/A"
        weight = f"{player.weight_pounds} lbs" if player.weight_pounds else "N/A"
        
        rows.append([
            player.id,
            player.full_name,
            player.position or "N/A",
            player.height_formatted,
            weight,
            team_name
        ])
    
    return tabulate(rows, headers=headers, tablefmt="grid")


def format_team_table(teams: List[Team]) -> str:
    """Format teams data as a table"""
    if not teams:
        return "No teams found."
    
    headers = ["ID", "Team", "City", "Conference", "Division"]
    rows = []
    
    for team in teams:
        rows.append([
            team.id,
            f"{team.name} ({team.abbreviation})",
            team.city,
            team.conference,
            team.division
        ])
    
    return tabulate(rows, headers=headers, tablefmt="grid")


def format_game_table(games: List[Game]) -> str:
    """Format games data as a table"""
    if not games:
        return "No games found."
    
    headers = ["ID", "Date", "Matchup", "Score", "Status", "Season"]
    rows = []
    
    for game in games:
        score = f"{game.visitor_team_score} - {game.home_team_score}"
        matchup = f"{game.visitor_team.abbreviation} @ {game.home_team.abbreviation}"
        
        rows.append([
            game.id,
            game.date,
            matchup,
            score,
            game.status,
            f"{game.season}-{game.season+1}"
        ])
    
    return tabulate(rows, headers=headers, tablefmt="grid")


@click.group()
@click.version_option(version="1.0.0")
def main():
    """
    🏀 SimpleNBA-API - Your command-line NBA data companion!
    
    Search for players, teams, games, and statistics using the BALLDONTLIE API.
    """
    pass


@main.command()
@click.option('--search', '-s', help='Search for players by name')
@click.option('--page', '-p', default=1, help='Page number (default: 1)')
@click.option('--limit', '-l', default=10, help='Number of results per page (default: 10)')
def players(search, page, limit):
    """Search for NBA players"""
    try:
        api = NBAAPI()
        
        if search:
            info_print(f"Searching for players matching '{search}'...")
        else:
            info_print("Fetching NBA players...")
        
        result = api.search_players(search=search, page=page, per_page=limit)
        
        if result['players']:
            success_print(f"Found {result['pagination']['total_count']} players")
            click.echo()
            click.echo(format_player_table(result['players']))
            
            # Show pagination info
            pagination = result['pagination']
            if pagination['total_pages'] > 1:
                click.echo()
                info_print(f"Page {pagination['current_page']} of {pagination['total_pages']}")
        else:
            warning_print("No players found matching your criteria.")
    
    except NBAAPIError as e:
        error_print(f"API Error: {e}")
        sys.exit(1)
    except Exception as e:
        error_print(f"Unexpected error: {e}")
        sys.exit(1)


@main.command()
@click.option('--conference', '-c', type=click.Choice(['East', 'West']), help='Filter by conference')
@click.option('--division', '-d', help='Filter by division')
def teams(conference, division):
    """List all NBA teams"""
    try:
        api = NBAAPI()
        info_print("Fetching NBA teams...")
        
        all_teams = api.get_all_teams()
        
        # Apply filters
        filtered_teams = all_teams
        if conference:
            filtered_teams = [t for t in filtered_teams if t.conference == conference]
        if division:
            filtered_teams = [t for t in filtered_teams if t.division.lower() == division.lower()]
        
        if filtered_teams:
            success_print(f"Found {len(filtered_teams)} teams")
            click.echo()
            click.echo(format_team_table(filtered_teams))
        else:
            warning_print("No teams found matching your criteria.")
    
    except NBAAPIError as e:
        error_print(f"API Error: {e}")
        sys.exit(1)
    except Exception as e:
        error_print(f"Unexpected error: {e}")
        sys.exit(1)


@main.command()
@click.option('--season', '-s', type=int, help='Season year (e.g., 2023)')
@click.option('--team', '-t', help='Team abbreviation (e.g., LAL)')
@click.option('--start-date', help='Start date (YYYY-MM-DD)')
@click.option('--end-date', help='End date (YYYY-MM-DD)')
@click.option('--postseason', is_flag=True, help='Show only postseason games')
@click.option('--limit', '-l', default=10, help='Number of results (default: 10)')
def games(season, team, start_date, end_date, postseason, limit):
    """Search for NBA games"""
    try:
        api = NBAAPI()
        
        # Get team ID if team abbreviation provided
        team_ids = None
        if team:
            all_teams = api.get_all_teams()
            team_obj = next((t for t in all_teams if t.abbreviation.upper() == team.upper()), None)
            if team_obj:
                team_ids = [team_obj.id]
                info_print(f"Searching games for {team_obj.full_name}...")
            else:
                error_print(f"Team '{team}' not found")
                return
        else:
            info_print("Searching for NBA games...")
        
        seasons = [season] if season else None
        
        result = api.get_games(
            seasons=seasons,
            team_ids=team_ids,
            start_date=start_date,
            end_date=end_date,
            postseason=postseason,
            per_page=limit
        )
        
        if result['games']:
            success_print(f"Found {result['pagination']['total_count']} games")
            click.echo()
            click.echo(format_game_table(result['games']))
        else:
            warning_print("No games found matching your criteria.")
    
    except NBAAPIError as e:
        error_print(f"API Error: {e}")
        sys.exit(1)
    except Exception as e:
        error_print(f"Unexpected error: {e}")
        sys.exit(1)


@main.command()
@click.argument('first_name')
@click.argument('last_name')
@click.option('--season', '-s', type=int, help='Season year for stats (e.g., 2023)')
def player_info(first_name, last_name, season):
    """Get detailed information about a specific player"""
    try:
        api = NBAAPI()
        
        info_print(f"Searching for player: {first_name} {last_name}")
        
        player = api.find_player_by_name(first_name, last_name)
        
        if not player:
            error_print(f"Player '{first_name} {last_name}' not found")
            return
        
        success_print(f"Found player: {player.full_name}")
        click.echo()
        
        # Display player info
        click.echo(f"{Fore.CYAN}Player Information:{Style.RESET_ALL}")
        info_data = [
            ["Name", player.full_name],
            ["ID", player.id],
            ["Position", player.position or "N/A"],
            ["Height", player.height_formatted],
            ["Weight", f"{player.weight_pounds} lbs" if player.weight_pounds else "N/A"],
            ["Team", str(player.team) if player.team else "N/A"]
        ]
        click.echo(tabulate(info_data, tablefmt="simple"))
        
        # Get season averages if season specified
        if season:
            click.echo()
            info_print(f"Fetching {season}-{season+1} season averages...")
            
            averages = api.get_season_averages(season, player.id)
            if averages:
                avg = averages[0]
                click.echo(f"{Fore.CYAN}Season Averages ({season}-{season+1}):{Style.RESET_ALL}")
                
                stats_data = [
                    ["Games", avg.get('games_played', 'N/A')],
                    ["Minutes", avg.get('min', 'N/A')],
                    ["Points", avg.get('pts', 'N/A')],
                    ["Rebounds", avg.get('reb', 'N/A')],
                    ["Assists", avg.get('ast', 'N/A')],
                    ["Steals", avg.get('stl', 'N/A')],
                    ["Blocks", avg.get('blk', 'N/A')],
                    ["FG%", f"{avg.get('fg_pct', 0)*100:.1f}%" if avg.get('fg_pct') else 'N/A'],
                    ["3P%", f"{avg.get('fg3_pct', 0)*100:.1f}%" if avg.get('fg3_pct') else 'N/A'],
                    ["FT%", f"{avg.get('ft_pct', 0)*100:.1f}%" if avg.get('ft_pct') else 'N/A']
                ]
                click.echo(tabulate(stats_data, tablefmt="simple"))
            else:
                warning_print(f"No season averages found for {season}-{season+1}")
    
    except NBAAPIError as e:
        error_print(f"API Error: {e}")
        sys.exit(1)
    except Exception as e:
        error_print(f"Unexpected error: {e}")
        sys.exit(1)


@main.command()
@click.argument('team_abbreviation')
def roster(team_abbreviation):
    """Get team roster"""
    try:
        api = NBAAPI()
        
        # Find team
        all_teams = api.get_all_teams()
        team = next((t for t in all_teams if t.abbreviation.upper() == team_abbreviation.upper()), None)
        
        if not team:
            error_print(f"Team '{team_abbreviation}' not found")
            return
        
        info_print(f"Fetching roster for {team.full_name}...")
        
        players = api.get_team_roster(team.id)
        
        if players:
            success_print(f"Found {len(players)} players on {team.full_name}")
            click.echo()
            click.echo(format_player_table(players))
        else:
            warning_print(f"No players found for {team.full_name}")
    
    except NBAAPIError as e:
        error_print(f"API Error: {e}")
        sys.exit(1)
    except Exception as e:
        error_print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()