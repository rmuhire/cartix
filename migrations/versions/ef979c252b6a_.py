"""empty message

Revision ID: ef979c252b6a
Revises: 2463083dc641
Create Date: 2017-04-19 16:32:37.199719

"""

# revision identifiers, used by Alembic.
revision = 'ef979c252b6a'
down_revision = '2463083dc641'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('finscope', sa.Column('year', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('finscope', 'year')
    ### end Alembic commands ###
