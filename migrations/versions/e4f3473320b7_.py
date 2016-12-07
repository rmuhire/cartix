"""empty message

Revision ID: e4f3473320b7
Revises: f85a5a2baa67
Create Date: 2016-12-06 18:34:37.959175

"""

# revision identifiers, used by Alembic.
revision = 'e4f3473320b7'
down_revision = 'f85a5a2baa67'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('files')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('files',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('original', sa.VARCHAR(length=25), autoincrement=False, nullable=True),
    sa.Column('saved', sa.VARCHAR(length=25), autoincrement=False, nullable=True),
    sa.Column('filename', sa.VARCHAR(length=150), autoincrement=False, nullable=True),
    sa.Column('regDate', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], [u'user.id'], name=u'files_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name=u'files_pkey')
    )
    ### end Alembic commands ###
