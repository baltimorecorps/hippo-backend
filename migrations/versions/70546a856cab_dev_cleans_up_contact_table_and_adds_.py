"""DEV cleans up Contact table and adds tables for about me

Revision ID: 70546a856cab
Revises: 7beedfdacaea
Create Date: 2020-07-06 15:48:55.542290

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '70546a856cab'
down_revision = '7beedfdacaea'
branch_labels = None
depends_on = None

address_type = postgresql.ENUM('home', 'work', name='AddressType')
status = postgresql.ENUM('active', 'inactive', name='Status')

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('profile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('contact_id', sa.Integer(), nullable=False),
    sa.Column('gender', sa.String(), nullable=True),
    sa.Column('gender_other', sa.String(), nullable=True),
    sa.Column('pronoun', sa.String(), nullable=True),
    sa.Column('pronoun_other', sa.String(), nullable=True),
    sa.Column('years_exp', sa.String(), nullable=True),
    sa.Column('job_search_status', sa.String(), nullable=True),
    sa.Column('current_job_status', sa.String(), nullable=True),
    sa.Column('current_edu_status', sa.String(), nullable=True),
    sa.Column('previous_bcorps_program', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('contact_address',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('contact_id', sa.Integer(), nullable=False),
    sa.Column('profile_id', sa.Integer(), nullable=False),
    sa.Column('is_primary', sa.Boolean(), nullable=True),
    sa.Column('street1', sa.String(), nullable=True),
    sa.Column('street2', sa.String(), nullable=True),
    sa.Column('city', sa.String(), nullable=True),
    sa.Column('state', sa.String(), nullable=True),
    sa.Column('country', sa.String(), nullable=True),
    sa.Column('zip_code', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.ForeignKeyConstraint(['profile_id'], ['profile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('race',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('contact_id', sa.Integer(), nullable=False),
    sa.Column('profile_id', sa.Integer(), nullable=False),
    sa.Column('american_indian', sa.Boolean(), nullable=True),
    sa.Column('asian', sa.Boolean(), nullable=True),
    sa.Column('black', sa.Boolean(), nullable=True),
    sa.Column('hawaiin', sa.Boolean(), nullable=True),
    sa.Column('hispanic', sa.Boolean(), nullable=True),
    sa.Column('south_asian', sa.Boolean(), nullable=True),
    sa.Column('white', sa.Boolean(), nullable=True),
    sa.Column('not_listed', sa.Boolean(), nullable=True),
    sa.Column('race_other', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.ForeignKeyConstraint(['profile_id'], ['profile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('role_choice',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('profile_id', sa.Integer(), nullable=False),
    sa.Column('advocacy_public_policy', sa.Boolean(), nullable=True),
    sa.Column('community_engagement_outreach', sa.Boolean(), nullable=True),
    sa.Column('data_analysis', sa.Boolean(), nullable=True),
    sa.Column('fundraising_development', sa.Boolean(), nullable=True),
    sa.Column('marketing_public_relations', sa.Boolean(), nullable=True),
    sa.Column('program_management', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['profile_id'], ['profile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('address')
    status.drop(op.get_bind(), checkfirst=False)
    address_type.drop(op.get_bind(), checkfirst=False)
    op.add_column('contact', sa.Column('email', sa.String(), nullable=True))
    op.add_column('contact', sa.Column('stage', sa.Integer(), nullable=True))
    op.drop_column('contact', 'pronouns')
    op.drop_column('contact', 'gender_other')
    op.drop_column('contact', 'gender')
    op.drop_column('contact', 'race_other')
    op.drop_column('contact', 'race_all')
    op.drop_column('contact', 'birthdate')
    op.drop_column('contact', 'salutation')
    op.drop_column('contact', 'pronouns_other')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contact', sa.Column('pronouns_other', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('contact', sa.Column('salutation', postgresql.ENUM('miss', 'mrs', 'mr', 'ms', 'dr', name='Salutation'), autoincrement=False, nullable=True))
    op.add_column('contact', sa.Column('birthdate', sa.DATE(), autoincrement=False, nullable=True))
    op.add_column('contact', sa.Column('race_all', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('contact', sa.Column('race_other', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('contact', sa.Column('gender', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.add_column('contact', sa.Column('gender_other', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('contact', sa.Column('pronouns', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.drop_column('contact', 'stage')
    op.drop_column('contact', 'email')
    op.create_table('address',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('contact_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('is_primary', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('street1', sa.VARCHAR(length=200), autoincrement=False, nullable=False),
    sa.Column('street2', sa.VARCHAR(length=200), autoincrement=False, nullable=True),
    sa.Column('city', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('state', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('country', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('postal_code', sa.VARCHAR(length=10), autoincrement=False, nullable=False),
    sa.Column('type', postgresql.ENUM('home', 'work', name='AddressType'), autoincrement=False, nullable=True),
    sa.Column('status', postgresql.ENUM('active', 'inactive', name='Status'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], name='address_contact_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='address_pkey')
    )
    op.drop_table('role_choice')
    op.drop_table('race')
    op.drop_table('contact_address')
    op.drop_table('profile')
    # ### end Alembic commands ###