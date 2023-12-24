from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy import create_engine, Column, Integer,String, ForeignKey, func, case, select, func, case, and_
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app import db

class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    profile_picture: so.Mapped[str] = so.mapped_column(sa.String(128), nullable=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    # create a method to calculate the user record, since each user has a squad
    # use the sqlachelmy relationship to get the squad 
    # and the ORM to do a group by to calculate the user's squad record
    def get_squad_record(self):
        overall_wins = func.sum(case([(Game.team_win == True, 1)], else_=0)).label('overall_wins')
        overall_losses = func.sum(case([(Game.team_win == False, 1)], else_=0)).label('overall_losses')
        win_pct = (func.sum(case([(Game.team_win == True, 1)], else_=0)) /
                   func.count(Game.id)).label('win_pct')

        query = select([
            overall_wins,
            overall_losses,
            win_pct
        ]).select_from(
            User
        ).join(
            Squad, Squad.user_id == User.id
        ).join(
            Team, Squad.team_id == Team.id
        ).join(
            Game, Team.id == Game.team_id
        ).where(
            User.id == self.id
        ).group_by(
            User.id
        )

        result = db.engine.execute(query).fetchone()

        if result:
            return {
                'overall_wins': result.overall_wins or 0,
                'overall_losses': result.overall_losses or 0,
                'win_pct': result.win_pct or 0 if result.win_pct is not None else 0
            }
        else:
            return {'overall_wins': 0, 'overall_losses': 0, 'win_pct': 0}




class Team(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    abbreviation: so.Mapped[str] = so.mapped_column(sa.String(5), index=True, unique=True)
    logo_link: so.Mapped[str] = so.mapped_column(sa.String(128), index=True, unique=True)

    # create a method to calculate the team record
    def get_record(self):
        # Assuming each squad has one team for simplicity
        games = Game.query.filter_by(team_id=self.id).all()
        
        wins = 0
        losses = 0
        for game in games:
            if game.team_win:
                wins += 1
            else:
                losses += 1

        return {'wins': wins, 'losses': losses, 'win_pct': wins / (wins + losses)}

class Squad(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    team_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('team.id'))
    team: so.Mapped[Team] = so.relationship('Team', backref='squads')
    user_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('user.id'))
    user: so.Mapped[User] = so.relationship('User', backref='squads')

class SquadName(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique = True)
    squad_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('squad.id'))
    squad: so.Mapped[Squad] = so.relationship('Squad', backref='squad_names')

class Game(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    gameid: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    date: so.Mapped[datetime] = so.mapped_column(sa.DateTime)
    team_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('team.id'))
    team = relationship('Team', foreign_keys=[team_id])
    team_score: so.Mapped[int] = so.mapped_column(sa.Integer)
    team_win: so.Mapped[bool] = so.mapped_column(sa.Boolean)