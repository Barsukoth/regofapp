"""empty message

Revision ID: c0360e766f03
Revises: 8846ebb3b4ca
Create Date: 2022-06-09 05:00:05.583993

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0360e766f03'
down_revision = '8846ebb3b4ca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_post_timestamp', table_name='post')
    op.drop_table('post')
    op.add_column('user', sa.Column('fullname', sa.String(length=128), nullable=True))
    op.drop_index('ix_user_username', table_name='user')
    op.create_index(op.f('ix_user_fullname'), 'user', ['fullname'], unique=True)
    op.drop_column('user', 'username')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('username', sa.VARCHAR(length=64), nullable=True))
    op.drop_index(op.f('ix_user_fullname'), table_name='user')
    op.create_index('ix_user_username', 'user', ['username'], unique=False)
    op.drop_column('user', 'fullname')
    op.create_table('post',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('body', sa.VARCHAR(length=140), nullable=True),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_post_timestamp', 'post', ['timestamp'], unique=False)
    # ### end Alembic commands ###