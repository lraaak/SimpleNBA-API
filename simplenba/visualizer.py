"""
Data visualization utilities for NBA statistics
"""

import matplotlib.pyplot as plt
import matplotlib.style as style
import pandas as pd
from typing import List, Dict, Any, Optional
from .models import Player, PlayerStats, Game, Team


class NBAVisualizer:
    """NBA data visualization class"""
    
    def __init__(self, style_name: str = 'seaborn-v0_8'):
        """
        Initialize the visualizer
        
        Args:
            style_name: Matplotlib style to use
        """
        try:
            plt.style.use(style_name)
        except:
            plt.style.use('default')
        
        # NBA colors
        self.colors = {
            'primary': '#1f77b4',
            'secondary': '#ff7f0e',
            'accent': '#2ca02c',
            'warning': '#d62728',
            'info': '#9467bd'
        }
    
    def plot_player_stats_comparison(self, players_stats: List[Dict[str, Any]], 
                                   stats: List[str] = None, 
                                   save_path: Optional[str] = None) -> str:
        """
        Create a radar chart comparing player statistics
        
        Args:
            players_stats: List of player season averages
            stats: List of stats to compare
            save_path: Path to save the plot
            
        Returns:
            Path to the saved plot
        """
        if not stats:
            stats = ['pts', 'reb', 'ast', 'stl', 'blk']
        
        if not players_stats:
            raise ValueError("No player stats provided")
        
        # Create DataFrame
        df_data = []
        for player_stat in players_stats:
            player_data = {'player': f"{player_stat.get('player_id', 'Unknown')}"}
            for stat in stats:
                player_data[stat] = player_stat.get(stat, 0) or 0
            df_data.append(player_data)
        
        df = pd.DataFrame(df_data)
        
        # Create the plot
        fig, ax = plt.subplots(figsize=(10, 6))
        
        x = range(len(stats))
        width = 0.35
        
        for i, player_data in enumerate(df_data):
            values = [player_data[stat] for stat in stats]
            ax.bar([xi + i * width for xi in x], values, width, 
                   label=player_data['player'], alpha=0.8)
        
        ax.set_xlabel('Statistics')
        ax.set_ylabel('Values')
        ax.set_title('Player Statistics Comparison')
        ax.set_xticks([xi + width/2 for xi in x])
        ax.set_xticklabels([stat.upper() for stat in stats])
        ax.legend()
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            save_path = '/tmp/player_comparison.png'
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.close()
        return save_path
    
    def plot_team_performance(self, games: List[Game], team: Team, 
                            save_path: Optional[str] = None) -> str:
        """
        Plot team performance over games
        
        Args:
            games: List of games
            team: Team to analyze
            save_path: Path to save the plot
            
        Returns:
            Path to the saved plot
        """
        if not games:
            raise ValueError("No games provided")
        
        # Prepare data
        dates = []
        scores = []
        opponent_scores = []
        wins = []
        
        for game in games:
            if game.status == "Final":
                dates.append(game.date)
                
                if game.home_team.id == team.id:
                    scores.append(game.home_team_score)
                    opponent_scores.append(game.visitor_team_score)
                    wins.append(game.home_team_score > game.visitor_team_score)
                else:
                    scores.append(game.visitor_team_score)
                    opponent_scores.append(game.home_team_score)
                    wins.append(game.visitor_team_score > game.home_team_score)
        
        if not scores:
            raise ValueError("No completed games found")
        
        # Create the plot
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # Score comparison
        x = range(len(scores))
        ax1.plot(x, scores, 'o-', label=f'{team.abbreviation} Score', 
                color=self.colors['primary'], linewidth=2, markersize=6)
        ax1.plot(x, opponent_scores, 'o-', label='Opponent Score', 
                color=self.colors['secondary'], linewidth=2, markersize=6)
        
        # Highlight wins and losses
        for i, win in enumerate(wins):
            color = self.colors['accent'] if win else self.colors['warning']
            ax1.axvspan(i-0.4, i+0.4, alpha=0.2, color=color)
        
        ax1.set_xlabel('Game Number')
        ax1.set_ylabel('Score')
        ax1.set_title(f'{team.full_name} - Game Scores')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Win/Loss record
        cumulative_wins = []
        win_count = 0
        for win in wins:
            if win:
                win_count += 1
            cumulative_wins.append(win_count / (len(cumulative_wins) + 1))
        
        ax2.plot(x, cumulative_wins, 'o-', color=self.colors['accent'], 
                linewidth=2, markersize=6)
        ax2.axhline(y=0.5, color='gray', linestyle='--', alpha=0.7)
        ax2.set_xlabel('Game Number')
        ax2.set_ylabel('Win Percentage')
        ax2.set_title(f'{team.full_name} - Win Percentage Over Time')
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(0, 1)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            save_path = f'/tmp/{team.abbreviation}_performance.png'
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.close()
        return save_path
    
    def plot_season_stats_trend(self, stats: List[PlayerStats], player: Player,
                              stat_name: str = 'pts', save_path: Optional[str] = None) -> str:
        """
        Plot a player's statistics trend over a season
        
        Args:
            stats: List of player statistics
            player: Player object
            stat_name: Statistics to plot
            save_path: Path to save the plot
            
        Returns:
            Path to the saved plot
        """
        if not stats:
            raise ValueError("No statistics provided")
        
        # Prepare data
        dates = []
        values = []
        
        for stat in stats:
            if hasattr(stat, stat_name) and getattr(stat, stat_name) is not None:
                dates.append(stat.game.date)
                values.append(getattr(stat, stat_name))
        
        if not values:
            raise ValueError(f"No {stat_name} data found")
        
        # Sort by date
        sorted_data = sorted(zip(dates, values))
        dates, values = zip(*sorted_data)
        
        # Create the plot
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x = range(len(values))
        ax.plot(x, values, 'o-', color=self.colors['primary'], 
               linewidth=2, markersize=6, alpha=0.8)
        
        # Add trend line
        if len(values) > 1:
            z = pd.Series(values).rolling(window=5, center=True).mean()
            ax.plot(x, z, '--', color=self.colors['secondary'], 
                   linewidth=2, alpha=0.7, label='5-game average')
        
        # Add average line
        avg_value = sum(values) / len(values)
        ax.axhline(y=avg_value, color=self.colors['accent'], 
                  linestyle=':', alpha=0.7, label=f'Season avg: {avg_value:.1f}')
        
        ax.set_xlabel('Game Number')
        ax.set_ylabel(stat_name.upper())
        ax.set_title(f'{player.full_name} - {stat_name.upper()} Trend')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            save_path = f'/tmp/{player.last_name}_{stat_name}_trend.png'
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.close()
        return save_path