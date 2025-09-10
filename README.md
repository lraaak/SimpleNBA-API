# 🏀 SimpleNBA-API

A comprehensive NBA API application for searching players, teams, and game history using the BALLDONTLIE API. Features both a command-line interface and a beautiful web application.

[![CI/CD Pipeline](https://github.com/lraaak/SimpleNBA-API/actions/workflows/ci.yml/badge.svg)](https://github.com/lraaak/SimpleNBA-API/actions/workflows/ci.yml)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- 🔍 **Advanced Player Search** - Find NBA players by name with detailed statistics
- 🏆 **Team Information** - Browse all 30 NBA teams by conference and division
- 📅 **Game History** - Access comprehensive game results with filtering options
- 📊 **Statistics & Analytics** - Season averages, player comparisons, and data visualization
- 💻 **CLI Interface** - Powerful command-line tools for data access
- 🌐 **Web Interface** - Beautiful, responsive web application
- 📈 **Data Export** - Export data to CSV format
- 🐳 **Docker Support** - Easy deployment with Docker
- 🧪 **Comprehensive Testing** - Full test suite with CI/CD pipeline

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/lraaak/SimpleNBA-API.git
cd SimpleNBA-API

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Command Line Usage

```bash
# Search for players
nba-cli players --search "LeBron James"

# List all teams
nba-cli teams

# Filter teams by conference
nba-cli teams --conference East

# Search for games
nba-cli games --season 2023 --team LAL

# Get detailed player information
nba-cli player-info LeBron James --season 2023

# Get team roster
nba-cli roster LAL
```

### Web Application

```bash
# Start the web server
python -m simplenba.webapp

# Or using Flask directly
export FLASK_APP=simplenba.webapp:create_app
flask run
```

Then visit `http://localhost:5000` in your browser.

### Docker Usage

```bash
# Build the Docker image
docker build -t simplenba-api .

# Run the container
docker run -p 5000:5000 simplenba-api
```

## 📖 API Usage

### Python Library

```python
from simplenba import NBAAPI

# Initialize the API client
api = NBAAPI()

# Search for players
result = api.search_players(search="LeBron James")
players = result['players']

# Get all teams
teams = api.get_all_teams()

# Get games for a specific team and season
games_result = api.get_games(seasons=[2023], team_ids=[1])
games = games_result['games']

# Get player statistics
stats_result = api.get_player_stats(player_ids=[123], seasons=[2023])
stats = stats_result['stats']

# Get season averages
averages = api.get_season_averages(season=2023, player_id=123)
```

### Data Models

The library provides clean data models for all NBA entities:

```python
# Player model
player = Player(
    id=123,
    first_name="LeBron",
    last_name="James",
    position="F",
    height_feet=6,
    height_inches=9,
    weight_pounds=250,
    team=team_object
)

print(player.full_name)  # "LeBron James"
print(player.height_formatted)  # "6'9""

# Team model
team = Team(
    id=1,
    abbreviation="LAL",
    city="Los Angeles",
    conference="West",
    division="Pacific",
    full_name="Los Angeles Lakers",
    name="Lakers"
)

# Game model
game = Game(
    id=456,
    date="2023-01-15",
    home_team=home_team,
    visitor_team=visitor_team,
    home_team_score=110,
    visitor_team_score=105,
    status="Final"
)

print(game.winner)  # Returns winning team
```

## 🛠️ CLI Commands

### Players

```bash
# Search players
nba-cli players --search "Stephen Curry" --limit 5

# Browse all players with pagination
nba-cli players --page 2 --limit 20
```

### Teams

```bash
# List all teams
nba-cli teams

# Filter by conference
nba-cli teams --conference West

# Filter by division
nba-cli teams --division Pacific
```

### Games

```bash
# Get games for specific season
nba-cli games --season 2023

# Filter by team
nba-cli games --team LAL --limit 10

# Filter by date range
nba-cli games --start-date 2023-01-01 --end-date 2023-01-31

# Postseason games only
nba-cli games --postseason --season 2023
```

### Player Information

```bash
# Get detailed player info
nba-cli player-info LeBron James

# Include season statistics
nba-cli player-info Stephen Curry --season 2023
```

### Team Roster

```bash
# Get team roster
nba-cli roster LAL
```

## 🌐 Web Interface

The web application provides:

- **Home Page** - Overview and quick player search
- **Players Page** - Advanced player search with pagination
- **Player Detail** - Comprehensive player information and statistics
- **Teams Page** - Browse teams by conference and division
- **Team Detail** - Team information, roster, and recent games
- **Games Page** - Game search with advanced filtering

### Screenshots

*Note: Screenshots would be added here showing the web interface*

## 🔧 Advanced Features

### Data Export

```python
from simplenba.utils import export_players_to_csv, export_games_to_csv

# Export players to CSV
players = api.search_players(search="Lakers")['players']
export_players_to_csv(players, 'lakers_players.csv')

# Export games to CSV
games = api.get_games(team_ids=[1])['games']
export_games_to_csv(games, 'lakers_games.csv')
```

### Data Visualization

```python
from simplenba.visualizer import NBAVisualizer

visualizer = NBAVisualizer()

# Compare player statistics
players_stats = [
    api.get_season_averages(2023, player_id=123)[0],
    api.get_season_averages(2023, player_id=456)[0]
]
chart_path = visualizer.plot_player_stats_comparison(players_stats)

# Plot team performance
team = api.get_team(1)
games = api.get_games(team_ids=[1])['games']
performance_chart = visualizer.plot_team_performance(games, team)
```

### Statistical Analysis

```python
from simplenba.utils import calculate_team_record, get_player_averages

# Calculate team record
games = api.get_games(team_ids=[1])['games']
team = api.get_team(1)
record = calculate_team_record(games, team)
print(f"Record: {record['wins']}-{record['losses']}")

# Get player averages
stats = api.get_player_stats(player_ids=[123])['stats']
averages = get_player_averages(stats)
print(f"PPG: {averages['pts']}")
```

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=simplenba --cov-report=html

# Run specific test file
python -m pytest tests/test_simplenba.py
```

## 📁 Project Structure

```
SimpleNBA-API/
├── simplenba/              # Main package
│   ├── __init__.py         # Package initialization
│   ├── api.py              # Core API client
│   ├── models.py           # Data models
│   ├── cli.py              # Command-line interface
│   ├── webapp.py           # Web application
│   ├── visualizer.py       # Data visualization
│   └── utils.py            # Utility functions
├── templates/              # Web interface templates
│   ├── base.html
│   ├── index.html
│   ├── players.html
│   ├── teams.html
│   └── games.html
├── tests/                  # Test suite
│   ├── __init__.py
│   ├── test_simplenba.py
│   └── README.md
├── docs/                   # Documentation
├── .github/workflows/      # CI/CD pipeline
├── requirements.txt        # Python dependencies
├── setup.py               # Package setup
├── Dockerfile             # Docker configuration
├── .gitignore             # Git ignore rules
├── LICENSE                # MIT License
└── README.md              # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 API Rate Limiting

The BALLDONTLIE API has rate limiting in place. This library includes:

- Built-in rate limiting (0.6 seconds between requests)
- Configurable delay settings
- Proper error handling for rate limit exceeding

## 🐛 Error Handling

The library provides comprehensive error handling:

```python
from simplenba.api import NBAAPIError

try:
    players = api.search_players(search="Invalid Player")
except NBAAPIError as e:
    print(f"API Error: {e}")
```

## 📊 Data Sources

This application uses the [BALLDONTLIE API](https://www.balldontlie.io/), which provides:

- Current and historical NBA player data
- Team information and rosters
- Game results and statistics
- Season averages and advanced stats

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [BALLDONTLIE API](https://www.balldontlie.io/) for providing comprehensive NBA data
- The NBA for creating an amazing sport with rich statistical data
- All contributors and users of this project

## 📞 Support

If you encounter any issues or have questions:

1. Check the [GitHub Issues](https://github.com/lraaak/SimpleNBA-API/issues)
2. Create a new issue if your problem isn't already reported
3. Provide as much detail as possible including error messages and steps to reproduce

---

Made with ❤️ for NBA fans and data enthusiasts!
