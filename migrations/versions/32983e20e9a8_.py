"""empty message

Revision ID: 32983e20e9a8
Revises: 1c0cb1ea3518
Create Date: 2016-12-14 19:55:27.742067

"""

# revision identifiers, used by Alembic.
revision = '32983e20e9a8'
down_revision = '1c0cb1ea3518'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'update_key')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('update_key', sa.VARCHAR(length=60), autoincrement=False, nullable=True))
    ### end Alembic commands ###
