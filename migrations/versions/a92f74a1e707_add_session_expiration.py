"""empty message

Revision ID: a92f74a1e707
Revises: e1e5db6b0a33
Create Date: 2020-01-29 17:00:00.164583

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a92f74a1e707'
down_revision = 'e1e5db6b0a33'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_session', sa.Column('expiration', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_session', 'expiration')
    # ### end Alembic commands ###
