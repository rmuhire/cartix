"""empty message

Revision ID: 4bf1aea270d5
Revises: 5850e27ce672
Create Date: 2017-04-19 16:34:39.415854

"""

# revision identifiers, used by Alembic.
revision = '4bf1aea270d5'
down_revision = '5850e27ce672'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('finscope',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('banked', sa.Integer(), nullable=True),
    sa.Column('other_formal', sa.Integer(), nullable=True),
    sa.Column('other_informal', sa.Integer(), nullable=True),
    sa.Column('excluded', sa.Integer(), nullable=True),
    sa.Column('year', sa.Integer(), nullable=True),
    sa.Column('district_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['district_id'], ['district.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('finscope')
    ### end Alembic commands ###
