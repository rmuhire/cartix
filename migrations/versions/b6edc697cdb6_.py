"""empty message

Revision ID: b6edc697cdb6
Revises: 32f83396ccfa
Create Date: 2017-03-06 15:41:32.497078

"""

# revision identifiers, used by Alembic.
revision = 'b6edc697cdb6'
down_revision = '32f83396ccfa'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'saving_group_funding_id_fkey', 'saving_group', type_='foreignkey')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(u'saving_group_funding_id_fkey', 'saving_group', 'ngo', ['funding_id'], ['id'])
    ### end Alembic commands ###
