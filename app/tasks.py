from nba_api.stats.static import teams
import pandas as pd
from nba_api.stats.endpoints import leaguegamefinder
import datetime
from datetime import date, timedelta
from app import db
from app.models import Game, Team, Squad, SquadName, User

def get_games_from_day(day, current_season):

    # Query for games in the current season
    gamefinder = leaguegamefinder.LeagueGameFinder()
    # The first DataFrame of those returned is what we want.
    games = gamefinder.get_data_frames()[0]
    games = games.loc[games['SEASON_ID'] == current_season]

    games_from_day = games[games.GAME_DATE == day]
    return(games_from_day[['TEAM_ABBREVIATION','TEAM_NAME','PTS', 'MATCHUP', 'GAME_DATE', 'WL', 'GAME_ID']])

def get_games_from_date_range(start_date, end_date, current_season):
    # Query for games in the current season
    gamefinder = leaguegamefinder.LeagueGameFinder()
    # The first DataFrame of those returned is what we want.
    games = gamefinder.get_data_frames()[0]
    games = games.loc[games['SEASON_ID'] == current_season]

    games_from_date_range = games[(games.GAME_DATE >= start_date) & (games.GAME_DATE <= end_date)]
    return(games_from_date_range[['TEAM_ABBREVIATION','TEAM_NAME','PTS', 'MATCHUP', 'GAME_DATE', 'WL','GAME_ID']])

def insert_games_into_db(games):
    for index, row in games.iterrows():
        # The columns in game are id, gameid, date, team_id, team_score, team_win
        game = Game(
            date=row['GAME_DATE'],
            gameid=row['GAME_ID'],
            team_id=Team.query.filter_by(abbreviation=row['TEAM_ABBREVIATION']).first().id,
            team_score=row['PTS'],
            team_win=(row['WL'] == 'W')
        )
        db.session.add(game)
    db.session.commit()