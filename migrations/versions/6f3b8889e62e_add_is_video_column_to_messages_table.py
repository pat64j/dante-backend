"""add is_video column to messages table

Revision ID: 6f3b8889e62e
Revises: e32982ca9daa
Create Date: 2020-08-11 17:20:37.423662

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f3b8889e62e'
down_revision = 'e32982ca9daa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('messages', sa.Column('is_video', sa.Boolean(), nullable=False, server_default='True'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('messages', 'is_video')
    # ### end Alembic commands ###
