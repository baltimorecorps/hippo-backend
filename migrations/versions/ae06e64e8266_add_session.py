"""empty message

Revision ID: ae06e64e8266
Revises: 2be793fbf577
Create Date: 2020-01-30 19:26:19.361178

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae06e64e8266'
down_revision = '2be793fbf577'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_session',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('auth_id', sa.String(), nullable=False),
    sa.Column('contact_id', sa.Integer(), nullable=False),
    sa.Column('jwt', sa.String(length=1000), nullable=False),
    sa.Column('expiration', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_session')
    # ### end Alembic commands ###
