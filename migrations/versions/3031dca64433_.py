"""empty message

Revision ID: 3031dca64433
Revises: c535f7ee76d1
Create Date: 2019-10-28 13:22:22.631800

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3031dca64433'
down_revision = 'c535f7ee76d1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('resume', sa.Column('gdoc_id', sa.String(length=255), nullable=True))
    op.drop_column('resume', 'gdoc_link')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('resume', sa.Column('gdoc_link', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.drop_column('resume', 'gdoc_id')
    # ### end Alembic commands ###
