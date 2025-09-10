"""
Data models for NBA entities
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class Team:
    """NBA Team representation"""
    id: int
    abbreviation: str
    city: str
    conference: str
    division: str
    full_name: str
    name: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Team':
        return cls(
            id=data['id'],
            abbreviation=data['abbreviation'],
            city=data['city'],
            conference=data['conference'],
            division=data['division'],
            full_name=data['full_name'],
            name=data['name']
        )

    def __str__(self) -> str:
        return f"{self.full_name} ({self.abbreviation})"


@dataclass
class Player:
    """NBA Player representation"""
    id: int
    first_name: str
    last_name: str
    position: Optional[str]
    height_feet: Optional[int]
    height_inches: Optional[int]
    weight_pounds: Optional[int]
    team: Optional[Team]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Player':
        team = None
        if data.get('team'):
            team = Team.from_dict(data['team'])
        
        return cls(
            id=data['id'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            position=data.get('position'),
            height_feet=data.get('height_feet'),
            height_inches=data.get('height_inches'),
            weight_pounds=data.get('weight_pounds'),
            team=team
        )

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def height_formatted(self) -> str:
        if self.height_feet and self.height_inches:
            return f"{self.height_feet}'{self.height_inches}\""
        return "Unknown"

    def __str__(self) -> str:
        team_name = f" ({self.team.abbreviation})" if self.team else ""
        return f"{self.full_name}{team_name}"


@dataclass
class Game:
    """NBA Game representation"""
    id: int
    date: str
    home_team: Team
    visitor_team: Team
    home_team_score: int
    visitor_team_score: int
    period: int
    postseason: bool
    season: int
    status: str
    time: Optional[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Game':
        return cls(
            id=data['id'],
            date=data['date'],
            home_team=Team.from_dict(data['home_team']),
            visitor_team=Team.from_dict(data['visitor_team']),
            home_team_score=data['home_team_score'],
            visitor_team_score=data['visitor_team_score'],
            period=data['period'],
            postseason=data['postseason'],
            season=data['season'],
            status=data['status'],
            time=data.get('time')
        )

    @property
    def winner(self) -> Optional[Team]:
        if self.status == "Final":
            if self.home_team_score > self.visitor_team_score:
                return self.home_team
            elif self.visitor_team_score > self.home_team_score:
                return self.visitor_team
        return None

    def __str__(self) -> str:
        return f"{self.visitor_team.abbreviation} @ {self.home_team.abbreviation} ({self.date})"


@dataclass
class Season:
    """NBA Season representation"""
    year: int
    
    def __str__(self) -> str:
        return f"{self.year}-{self.year + 1} Season"


@dataclass
class PlayerStats:
    """Player statistics for a game"""
    id: int
    player: Player
    game: Game
    team: Team
    min: Optional[str]
    fgm: Optional[int]  # Field goals made
    fga: Optional[int]  # Field goals attempted
    fg3m: Optional[int]  # 3-point field goals made
    fg3a: Optional[int]  # 3-point field goals attempted
    ftm: Optional[int]  # Free throws made
    fta: Optional[int]  # Free throws attempted
    oreb: Optional[int]  # Offensive rebounds
    dreb: Optional[int]  # Defensive rebounds
    reb: Optional[int]  # Total rebounds
    ast: Optional[int]  # Assists
    stl: Optional[int]  # Steals
    blk: Optional[int]  # Blocks
    turnover: Optional[int]  # Turnovers
    pf: Optional[int]  # Personal fouls
    pts: Optional[int]  # Points

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PlayerStats':
        return cls(
            id=data['id'],
            player=Player.from_dict(data['player']),
            game=Game.from_dict(data['game']),
            team=Team.from_dict(data['team']),
            min=data.get('min'),
            fgm=data.get('fgm'),
            fga=data.get('fga'),
            fg3m=data.get('fg3m'),
            fg3a=data.get('fg3a'),
            ftm=data.get('ftm'),
            fta=data.get('fta'),
            oreb=data.get('oreb'),
            dreb=data.get('dreb'),
            reb=data.get('reb'),
            ast=data.get('ast'),
            stl=data.get('stl'),
            blk=data.get('blk'),
            turnover=data.get('turnover'),
            pf=data.get('pf'),
            pts=data.get('pts')
        )

    @property
    def fg_percentage(self) -> Optional[float]:
        if self.fga and self.fga > 0:
            return round((self.fgm / self.fga) * 100, 1)
        return None

    @property
    def fg3_percentage(self) -> Optional[float]:
        if self.fg3a and self.fg3a > 0:
            return round((self.fg3m / self.fg3a) * 100, 1)
        return None

    @property
    def ft_percentage(self) -> Optional[float]:
        if self.fta and self.fta > 0:
            return round((self.ftm / self.fta) * 100, 1)
        return None