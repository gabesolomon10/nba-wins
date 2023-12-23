from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app import db

class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
class Team(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    abbreviation: so.Mapped[str] = so.mapped_column(sa.String(5), index=True, unique=True)
    logo_link: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)

class Squad(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    team_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('team.id'))
    team: so.Mapped[Team] = so.relationship('Team', backref='squads')
    user_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('user.id'))
    user: so.Mapped[User] = so.relationship('User', backref='squads')

class Game(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    date: so.Mapped[datetime] = so.mapped_column(sa.DateTime, index=True, unique=True)
    home_team_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('team.id'))
    home_team = relationship('Team', foreign_keys=[home_team_id])
    away_team_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('team.id'))
    away_team = relationship('Team', foreign_keys=[away_team_id])
    home_team_score: so.Mapped[int] = so.mapped_column(sa.Integer)
    away_team_score: so.Mapped[int] = so.mapped_column(sa.Integer)
    home_team_win: so.Mapped[bool] = so.mapped_column(sa.Boolean)
    away_team_win: so.Mapped[bool] = so.mapped_column(sa.Boolean)