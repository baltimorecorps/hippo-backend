"""Adds cycle_id to opportunity table

Revision ID: eb6d9410ef2a
Revises: fec0987cfc79
Create Date: 2020-02-20 03:18:22.647544

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb6d9410ef2a'
down_revision = 'fec0987cfc79'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('opportunity', sa.Column('cycle_id', sa.Integer()))
    op.execute("UPDATE opportunity SET cycle_id = 1")
    op.create_foreign_key(None, 'opportunity', 'cycle', ['cycle_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('opportunity_cycle_id_fkey', 'opportunity', type_='foreignkey')
    op.drop_column('opportunity', 'cycle_id')
    # ### end Alembic commands ###