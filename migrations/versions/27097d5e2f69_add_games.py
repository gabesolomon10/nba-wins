"""add games

Revision ID: 27097d5e2f69
Revises: 1b0d09ca81b1
Create Date: 2023-12-24 08:55:07.704614

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '27097d5e2f69'
down_revision = '1b0d09ca81b1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.add_column(sa.Column('gameid', sa.String(length=64), nullable=False))
        batch_op.add_column(sa.Column('team_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('team_score', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('team_win', sa.Boolean(), nullable=False))
        batch_op.drop_index('ix_game_date')
        batch_op.create_index(batch_op.f('ix_game_gameid'), ['gameid'], unique=False)
        batch_op.drop_constraint('game_ibfk_2', type_='foreignkey')
        batch_op.drop_constraint('game_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'team', ['team_id'], ['id'])
        batch_op.drop_column('away_team_score')
        batch_op.drop_column('away_team_win')
        batch_op.drop_column('home_team_score')
        batch_op.drop_column('away_team_id')
        batch_op.drop_column('home_team_id')
        batch_op.drop_column('home_team_win')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.add_column(sa.Column('home_team_win', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('home_team_id', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('away_team_id', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('home_team_score', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('away_team_win', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('away_team_score', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('game_ibfk_1', 'team', ['away_team_id'], ['id'])
        batch_op.create_foreign_key('game_ibfk_2', 'team', ['home_team_id'], ['id'])
        batch_op.drop_index(batch_op.f('ix_game_gameid'))
        batch_op.create_index('ix_game_date', ['date'], unique=True)
        batch_op.drop_column('team_win')
        batch_op.drop_column('team_score')
        batch_op.drop_column('team_id')
        batch_op.drop_column('gameid')

    # ### end Alembic commands ###
