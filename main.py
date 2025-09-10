import requests

# Define the API endpoint for players
players_url = "https://api.balldontlie.io/v1/players"
teams_url = "https://api.balldontlie.io/v1/teams"
games_url = "https://api.balldontlie.io/v1/games"


# Your API key from Balldontlie (replace with your actual key)
api_key = "YOUR API KEY"
headers = {'Authorization': api_key}
nba_abv = ('ATL', 'BOS', 'BRK', 'CHI', 'CHO', 'CLE', 'DAL', 'DEN', 'DET', 'GSW',
           'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK', 
           'OKC', 'ORL', 'PHI', 'PHX', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS')

def get_players(per_page=10, cursor=None, search=None, first_name=None, last_name=None, team_ids=None, player_ids=None):
    params = {
        'per_page': per_page,
        'cursor': cursor,
        'search': search,
        'first_name': first_name,
        'last_name': last_name,
        'team_ids': team_ids,
        'player_ids': player_ids
    }
    
    try:
        response = requests.get(players_url, headers=headers, params=params)
        response.raise_for_status() 
        
    except requests.RequestException as e:
        print(f"Error fetching players: {e}")
        return {"error": str(e)}
    
    data = response.json()
    players = data.get('data', [])
    meta = data.get('meta', {})
    next_cursor = meta.get('next_cursor')

    for player in players:
        # Skip if team_ids[] is specified and player’s team is not in it
        team_ids = params.get('team_ids')
        if team_ids and player['team']['id'] not in team_ids:
            continue

        # Skip if player_ids[] is specified and player’s ID is not in it
        player_ids = params.get('player_ids')
        if player_ids and player['id'] not in player_ids:
            continue

        # Skip if first_name filter is specified and doesn't match (case-insensitive)
        first_name_filter = params.get('first_name')
        if first_name_filter and first_name_filter.lower() not in player['first_name'].lower():
            continue

        # Skip if last_name filter is specified and doesn't match (case-insensitive)
        last_name_filter = params.get('last_name')
        if last_name_filter and last_name_filter.lower() not in player['last_name'].lower():
            continue

        # Skip if search filter is specified and doesn’t match first or last name
        search_filter = params.get('search')
        if search_filter:
            search_lower = search_filter.lower()
            if search_lower not in player['first_name'].lower() and search_lower not in player['last_name'].lower():
                continue

        # Print player info
        print(f"ID: {player['id']}, Name: {player['first_name']} {player['last_name']}, "
            f"Team: {player['team']['full_name']}, Position: {player['position']}")
    
    return next_cursor


def get_teams(division=None, conference=None):
    
    params = {
        "division": division,
        "conference": conference
    }
    
    try:
        response = requests.get(teams_url, headers=headers, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching teams: {e}")
        return {"error": str(e)}
    
    data = response.json()
    teams = data.get('data', [])
    
    for team in teams:
        
        if division and team['division'] != division:
            continue
        if conference and team['conference'] != conference:
            continue
        
        print(f"ID: {team['id']}, Name: {team['full_name']}, Abbreviation: {team['abbreviation']}, "
                f"City: {team['city']}, Conference: {team['conference']}, Division: {team['division']}")
        
    return {"teams": teams}


def get_games(per_page=10, cursor=None, dates=None, seasons=None, team_ids=None, postseason=None, start_date=None, end_date=None):
    
    params = {
        'per_page': per_page,
        'cursor': cursor,
        'dates': dates, # List of dates in 'YYYY-MM-DD' format
        'seasons': seasons,
        'team_ids': team_ids,
        'postseason': postseason,
        'start_date': start_date,
        'end_date': end_date
    }
    
    try:
        response = requests.get(games_url, headers=headers, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching games: {e}")
        return {"error": str(e)}
    
    data = response.json()
    games = data.get('data', [])
    meta = data.get('meta', {})
    next_cursor = meta.get('next_cursor')
    
    for game in games:
        
        if (team_ids) and game['home_team']['id'] not in team_ids and game['visitor_team']['id'] not in team_ids:
            continue
        if (dates) and game['date'] not in dates:
            continue
        if (seasons) and game['season'] not in seasons:
            continue
        if (postseason is not None) and game['postseason'] != postseason:
            continue
        if (start_date) and game['date'] < start_date:
            continue
        if (end_date) and game['date'] > end_date:
            continue
        
        print(f"ID: {game['id']}, Date: {game['date']}, Season: {game['season']}, "
              f"Home Team: {game['home_team']['full_name']} ({game['home_team_score']}), "
              f"Visitor Team: {game['visitor_team']['full_name']} ({game['visitor_team_score']})")
        
    return next_cursor

def get_specific_game(id: int):
    
    url = f"{games_url}/{id}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching game {id}: {e}")
        return {"error": str(e)}
    
    game = response.json()
    print(f"ID: {game['id']}, Date: {game['date']}, Season: {game['season']}, "
          f"Home Team: {game['home_team']['full_name']} ({game['home_team_score']}), "
          f"Visitor Team: {game['visitor_team']['full_name']} ({game['visitor_team_score']})")
    
    

def main_menu():
    while True:
        print("\nNBA API Main Menu")
        print("1. Get Players")
        print("2. Get Teams")
        print("3. Get Games")
        print("4. Get Specific Game by ID")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()
        if not choice:
            print("No input detected. Please enter a number 1-5.")
            continue

        if choice == '1':
            per_page = input("Enter number of players per page (or press enter for default 10): ").strip()
            per_page = int(per_page) if per_page.isdigit() else 10

            search = input("Enter search term for player names (or press Enter to skip): ").strip() or None
            first_name = input("Enter first name filter (or press Enter to skip): ").strip() or None
            last_name = input("Enter last name filter (or press Enter to skip): ").strip() or None

            team_ids_input = input("Enter team IDs as comma-separated values (or press Enter to skip): ").strip()
            team_ids = [int(tid) for tid in team_ids_input.split(',') if tid.isdigit()] if team_ids_input else None

            player_ids_input = input("Enter player IDs as comma-separated values (or press Enter to skip): ").strip()
            player_ids = [int(pid) for pid in player_ids_input.split(',') if pid.isdigit()] if player_ids_input else None

            cursor = None  # start at the first page
            while True:
                next_cursor = get_players(per_page, cursor, search, first_name, last_name, team_ids, player_ids)
                
                if not next_cursor:
                    print("\nNo more pages available.")
                    break

                # Ask user if they want to go to next page
                print("\nOptions:")
                print("1. Next page")
                print("2. Return to main menu")

                next_choice = input("Enter your choice: ").strip()
                if not next_choice or next_choice != '1':
                    break  # Return to main menu
                cursor = next_cursor  # go to next page

        elif choice == '2':
            division = input("Enter division filter (or press Enter to skip): ").strip() or None
            conference = input("Enter conference filter (or press Enter to skip): ").strip() or None
            get_teams(division, conference)            
            
        elif choice == '3':
            per_page = input("Enter number of games per page (default 10): ").strip()
            per_page = int(per_page) if per_page.isdigit() else 10
            dates_input = input("Enter dates as comma-separated values in 'YYYY-MM-DD' format (or press Enter to skip): ").strip()
            dates = [date.strip() for date in dates_input.split(',')] if dates_input else None
            seasons_input = input("Enter seasons as comma-separated values (or press Enter to skip): ").strip()
            seasons = [int(season) for season in seasons_input.split(',') if season.isdigit()] if seasons_input else None
            team_ids_input = input("Enter team IDs as comma-separated values (or press Enter to skip): ").strip()
            team_ids = [int(tid) for tid in team_ids_input.split(',') if tid.isdigit()] if team_ids_input else None
            postseason_input = input("Enter 'yes' for postseason games, 'no' for regular season, or press Enter to skip: ").strip().lower()
            postseason = True if postseason_input == 'yes' else False if postseason_input == 'no' else None
            start_date = input("Enter start date in 'YYYY-MM-DD' format (or press Enter to skip): ").strip() or None
            end_date = input("Enter end date in 'YYYY-MM-DD' format (or press Enter to skip): ").strip() or None
            
            cursor = None
            
            while True:
                next_cursor = get_games(per_page, cursor, dates, seasons, team_ids, postseason, start_date, end_date)
                
                if not next_cursor:
                    print("\nNo more pages available.")
                    break

                # Ask user if they want to go to next page
                print("\nOptions:")
                print("1. Next page")
                print("2. Return to main menu")

                next_choice = input("Enter your choice: ").strip()
                if not next_choice or next_choice != '1':
                    break
                cursor = next_cursor
                
        elif choice == '4':
            # Get specific game
            game_id = input("Enter game ID: ").strip()
            if game_id.isdigit():
                get_specific_game(int(game_id))
            else:
                print("Invalid game ID.")

        elif choice == '5':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number 1-5.")

        
if __name__ == "__main__":
    main_menu()
