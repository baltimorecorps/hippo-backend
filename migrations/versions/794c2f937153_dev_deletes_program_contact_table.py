"""DEV deletes program_contact table

Revision ID: 794c2f937153
Revises: 0c0dd74f74a9
Create Date: 2020-10-28 14:59:43.655197

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '794c2f937153'
down_revision = '0c0dd74f74a9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('program_contact')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('program_contact',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('contact_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('program_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('card_id', sa.VARCHAR(length=25), autoincrement=False, nullable=True),
    sa.Column('stage', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('is_approved', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], name='program_contact_contact_id_fkey'),
    sa.ForeignKeyConstraint(['program_id'], ['program.id'], name='program_contact_program_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='program_contact_pkey')
    )
    # ### end Alembic commands ###
