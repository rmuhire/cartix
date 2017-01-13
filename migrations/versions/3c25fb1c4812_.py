"""empty message

Revision ID: 3c25fb1c4812
Revises: 887b0d8b4601
Create Date: 2017-01-13 15:20:32.507212

"""

# revision identifiers, used by Alembic.
revision = '3c25fb1c4812'
down_revision = '887b0d8b4601'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bank_agent', sa.Column('year', sa.Integer(), nullable=True))
    op.add_column('financial', sa.Column('year', sa.Integer(), nullable=True))
    op.add_column('population', sa.Column('year', sa.Integer(), nullable=True))
    op.add_column('telco_agent', sa.Column('year', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('telco_agent', 'year')
    op.drop_column('population', 'year')
    op.drop_column('financial', 'year')
    op.drop_column('bank_agent', 'year')
    ### end Alembic commands ###
