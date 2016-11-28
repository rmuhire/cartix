"""empty message

Revision ID: 6c7591de7f80
Revises: None
Create Date: 2016-11-28 11:03:31.039910

"""

# revision identifiers, used by Alembic.
revision = '6c7591de7f80'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ngo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=60), nullable=True),
    sa.Column('telephone', sa.String(length=30), nullable=True),
    sa.Column('website', sa.String(length=60), nullable=True),
    sa.Column('category', sa.String(length=40), nullable=True),
    sa.Column('picture', sa.String(length=100), nullable=True),
    sa.Column('address', sa.String(length=200), nullable=True),
    sa.Column('cp_name', sa.String(length=60), nullable=True),
    sa.Column('cp_email', sa.String(length=60), nullable=True),
    sa.Column('cp_telephone', sa.String(length=30), nullable=True),
    sa.Column('password', sa.String(length=40), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cp_email'),
    sa.UniqueConstraint('cp_telephone'),
    sa.UniqueConstraint('name')
    )
    op.create_table('saving_group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('year', sa.Integer(), nullable=True),
    sa.Column('member_female', sa.Integer(), nullable=True),
    sa.Column('member_male', sa.Integer(), nullable=True),
    sa.Column('sector_id', sa.Integer(), nullable=True),
    sa.Column('regDate', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('amount',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('saving', sa.Float(), nullable=True),
    sa.Column('borrowing', sa.Float(), nullable=True),
    sa.Column('year', sa.Integer(), nullable=True),
    sa.Column('sg_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['sg_id'], ['saving_group.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sgs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('partner_id', sa.Integer(), nullable=True),
    sa.Column('funding_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['funding_id'], ['ngo.id'], ),
    sa.ForeignKeyConstraint(['partner_id'], ['ngo.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sgs')
    op.drop_table('amount')
    op.drop_table('saving_group')
    op.drop_table('ngo')
    ### end Alembic commands ###
