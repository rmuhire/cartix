"""empty message

Revision ID: 8d62bddb0615
Revises: aa655a6f9f96
Create Date: 2017-04-04 16:21:10.069889

"""

# revision identifiers, used by Alembic.
revision = '8d62bddb0615'
down_revision = 'aa655a6f9f96'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bank', sa.Column('branch_counts', sa.Integer(), nullable=True))
    op.drop_column('bank', 'branch_count')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bank', sa.Column('branch_count', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.drop_column('bank', 'branch_counts')
    ### end Alembic commands ###
