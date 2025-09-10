"""
Flask web application for SimpleNBA-API
"""

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import json
from datetime import datetime

from .api import NBAAPI, NBAAPIError


def create_app():
    """Create and configure the Flask application"""
    import os
    template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
    app = Flask(__name__, template_folder=template_dir)
    app.secret_key = 'simplenba-api-secret-key'
    
    # Initialize NBA API
    nba_api = NBAAPI()
    
    @app.route('/')
    def index():
        """Home page"""
        return render_template('index.html')
    
    @app.route('/players')
    def players():
        """Players search page"""
        search = request.args.get('search', '')
        page = int(request.args.get('page', 1))
        
        try:
            result = nba_api.search_players(search=search if search else None, page=page, per_page=20)
            return render_template('players.html', 
                                 players=result['players'], 
                                 pagination=result['pagination'],
                                 search=search)
        except NBAAPIError as e:
            flash(f'API Error: {e}', 'error')
            return render_template('players.html', players=[], pagination={}, search=search)
    
    @app.route('/player/<int:player_id>')
    def player_detail(player_id):
        """Player detail page"""
        try:
            player = nba_api.get_player(player_id)
            if not player:
                flash('Player not found', 'error')
                return redirect(url_for('players'))
            
            # Get recent season averages (2023)
            season_averages = nba_api.get_season_averages(2023, player_id)
            
            return render_template('player_detail.html', 
                                 player=player, 
                                 season_averages=season_averages[0] if season_averages else None)
        except NBAAPIError as e:
            flash(f'API Error: {e}', 'error')
            return redirect(url_for('players'))
    
    @app.route('/teams')
    def teams():
        """Teams page"""
        conference = request.args.get('conference')
        
        try:
            all_teams = nba_api.get_all_teams()
            
            if conference:
                teams_list = [t for t in all_teams if t.conference == conference]
            else:
                teams_list = all_teams
            
            # Group teams by conference and division
            conferences = {}
            for team in teams_list:
                if team.conference not in conferences:
                    conferences[team.conference] = {}
                if team.division not in conferences[team.conference]:
                    conferences[team.conference][team.division] = []
                conferences[team.conference][team.division].append(team)
            
            return render_template('teams.html', conferences=conferences, selected_conference=conference)
        except NBAAPIError as e:
            flash(f'API Error: {e}', 'error')
            return render_template('teams.html', conferences={}, selected_conference=conference)
    
    @app.route('/team/<int:team_id>')
    def team_detail(team_id):
        """Team detail page"""
        try:
            team = nba_api.get_team(team_id)
            if not team:
                flash('Team not found', 'error')
                return redirect(url_for('teams'))
            
            # Get team roster
            roster = nba_api.get_team_roster(team_id)
            
            # Get recent games
            recent_games = nba_api.get_games(team_ids=[team_id], per_page=10)
            
            return render_template('team_detail.html', 
                                 team=team, 
                                 roster=roster, 
                                 recent_games=recent_games['games'])
        except NBAAPIError as e:
            flash(f'API Error: {e}', 'error')
            return redirect(url_for('teams'))
    
    @app.route('/games')
    def games():
        """Games page"""
        season = request.args.get('season', type=int)
        team = request.args.get('team')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        postseason = request.args.get('postseason') == 'on'
        page = int(request.args.get('page', 1))
        
        try:
            # Get team ID if team abbreviation provided
            team_ids = None
            team_obj = None
            if team:
                all_teams = nba_api.get_all_teams()
                team_obj = next((t for t in all_teams if t.abbreviation.upper() == team.upper()), None)
                if team_obj:
                    team_ids = [team_obj.id]
            
            seasons = [season] if season else None
            
            result = nba_api.get_games(
                seasons=seasons,
                team_ids=team_ids,
                start_date=start_date,
                end_date=end_date,
                postseason=postseason,
                page=page,
                per_page=20
            )
            
            # Get all teams for the filter dropdown
            all_teams = nba_api.get_all_teams()
            
            return render_template('games.html', 
                                 games=result['games'],
                                 pagination=result['pagination'],
                                 all_teams=all_teams,
                                 filters={
                                     'season': season,
                                     'team': team,
                                     'start_date': start_date,
                                     'end_date': end_date,
                                     'postseason': postseason
                                 })
        except NBAAPIError as e:
            flash(f'API Error: {e}', 'error')
            return render_template('games.html', games=[], pagination={}, all_teams=[], filters={})
    
    @app.route('/game/<int:game_id>')
    def game_detail(game_id):
        """Game detail page"""
        try:
            game = nba_api.get_game(game_id)
            if not game:
                flash('Game not found', 'error')
                return redirect(url_for('games'))
            
            return render_template('game_detail.html', game=game)
        except NBAAPIError as e:
            flash(f'API Error: {e}', 'error')
            return redirect(url_for('games'))
    
    # API endpoints for AJAX requests
    @app.route('/api/search_players')
    def api_search_players():
        """API endpoint for player search"""
        search = request.args.get('q', '')
        
        try:
            result = nba_api.search_players(search=search, per_page=10)
            return jsonify({
                'players': [
                    {
                        'id': p.id,
                        'name': p.full_name,
                        'team': p.team.abbreviation if p.team else None,
                        'position': p.position
                    }
                    for p in result['players']
                ]
            })
        except NBAAPIError:
            return jsonify({'players': []})
    
    @app.template_filter('format_percentage')
    def format_percentage(value):
        """Template filter to format percentages"""
        if value is None:
            return 'N/A'
        return f"{value * 100:.1f}%"
    
    @app.template_filter('format_date')
    def format_date(date_string):
        """Template filter to format dates"""
        try:
            date = datetime.strptime(date_string, '%Y-%m-%d')
            return date.strftime('%B %d, %Y')
        except:
            return date_string
    
    return app


def run_app(host='127.0.0.1', port=5000, debug=True):
    """Run the Flask application"""
    app = create_app()
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    run_app()