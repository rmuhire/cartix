"""empty message

Revision ID: d0d725ab6291
Revises: 3c25fb1c4812
Create Date: 2017-01-25 14:49:06.246687

"""

# revision identifiers, used by Alembic.
revision = 'd0d725ab6291'
down_revision = '3c25fb1c4812'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('files', sa.Column('status', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('files', 'status')
    ### end Alembic commands ###
