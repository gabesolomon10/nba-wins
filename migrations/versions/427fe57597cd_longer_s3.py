"""longer s3

Revision ID: 427fe57597cd
Revises: 7315fd150d07
Create Date: 2023-12-23 19:46:34.069751

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '427fe57597cd'
down_revision = '7315fd150d07'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('team', schema=None) as batch_op:
        batch_op.alter_column('logo_link',
               existing_type=mysql.VARCHAR(length=64),
               type_=sa.String(length=128),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('team', schema=None) as batch_op:
        batch_op.alter_column('logo_link',
               existing_type=sa.String(length=128),
               type_=mysql.VARCHAR(length=64),
               existing_nullable=False)

    # ### end Alembic commands ###