"""add other tables

Revision ID: 441ae8a1977d
Revises: 4993f6eda2d2
Create Date: 2023-12-23 15:08:58.042499

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '441ae8a1977d'
down_revision = '4993f6eda2d2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('team',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('abbreviation', sa.String(length=5), nullable=False),
    sa.Column('logo_link', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('team', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_team_abbreviation'), ['abbreviation'], unique=True)
        batch_op.create_index(batch_op.f('ix_team_logo_link'), ['logo_link'], unique=True)
        batch_op.create_index(batch_op.f('ix_team_name'), ['name'], unique=True)

    op.create_table('squad',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['team_id'], ['team.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('squad', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_squad_name'), ['name'], unique=True)

    op.create_table('game',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('home_team_id', sa.Integer(), nullable=False),
    sa.Column('away_team_id', sa.Integer(), nullable=False),
    sa.Column('home_team_score', sa.Integer(), nullable=False),
    sa.Column('away_team_score', sa.Integer(), nullable=False),
    sa.Column('home_team_win', sa.Boolean(), nullable=False),
    sa.Column('away_team_win', sa.Boolean(), nullable=False),
    sa.Column('home_team_squad_id', sa.Integer(), nullable=False),
    sa.Column('away_team_squad_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['away_team_id'], ['team.id'], ),
    sa.ForeignKeyConstraint(['away_team_squad_id'], ['squad.id'], ),
    sa.ForeignKeyConstraint(['home_team_id'], ['team.id'], ),
    sa.ForeignKeyConstraint(['home_team_squad_id'], ['squad.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_game_date'), ['date'], unique=True)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index('ix_user_teamname')
        batch_op.drop_column('teamname')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('teamname', mysql.VARCHAR(length=64), nullable=False))
        batch_op.create_index('ix_user_teamname', ['teamname'], unique=True)

    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_game_date'))

    op.drop_table('game')
    with op.batch_alter_table('squad', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_squad_name'))

    op.drop_table('squad')
    with op.batch_alter_table('team', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_team_name'))
        batch_op.drop_index(batch_op.f('ix_team_logo_link'))
        batch_op.drop_index(batch_op.f('ix_team_abbreviation'))

    op.drop_table('team')
    # ### end Alembic commands ###