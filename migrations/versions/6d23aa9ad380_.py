"""empty message

Revision ID: 6d23aa9ad380
Revises: 
Create Date: 2019-02-22 16:37:04.108107

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d23aa9ad380'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('mobile')
    op.alter_column('contact', 'phone_primary',
               existing_type=sa.VARCHAR(length=25),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('contact', 'phone_primary',
               existing_type=sa.VARCHAR(length=25),
               nullable=True)
    op.create_table('mobile',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('model', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('price', sa.REAL(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='mobile_pkey')
    )
    # ### end Alembic commands ###
