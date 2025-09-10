"""
SimpleNBA-API: A Python library for accessing NBA data via the BALLDONTLIE API
"""

__version__ = "1.0.0"
__author__ = "SimpleNBA-API"

from .api import NBAAPI
from .models import Player, Team, Game, Season

__all__ = ["NBAAPI", "Player", "Team", "Game", "Season"]