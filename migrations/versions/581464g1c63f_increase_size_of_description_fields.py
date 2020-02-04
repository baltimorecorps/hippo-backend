"""Increases size of description fields

Revision ID: 581464g1c63f
Revises: 671364b9b36c
Create Date: 2020-01-15

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '581464g1c63f'
down_revision = '671364b9b36c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('experience', 'description',
               existing_type=sa.VARCHAR(length=500),
               type_=sa.String(length=2000),
               existing_nullable=True,
               existing_server_default=sa.text(u"''::character varying"))
    op.alter_column('achievement', 'description',
               existing_type=sa.VARCHAR(length=500),
               type_=sa.String(length=2000),
               existing_nullable=True,
               existing_server_default=sa.text(u"''::character varying"))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('experience', 'description',
               existing_type=sa.VARCHAR(length=2000),
               type_=sa.String(length=500),
               existing_nullable=True,
               existing_server_default=sa.text(u"''::character varying"))
    op.alter_column('achievement', 'description',
               existing_type=sa.VARCHAR(length=2000),
               type_=sa.String(length=500),
               existing_nullable=True,
               existing_server_default=sa.text(u"''::character varying"))
    # ### end Alembic commands ###
