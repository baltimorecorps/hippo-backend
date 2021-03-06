"""empty message

Revision ID: 2f9c7b6ac02b
Revises: 
Create Date: 2019-09-23 16:04:26.570566

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f9c7b6ac02b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contact',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('salutation', sa.Enum('miss', 'mrs', 'mr', 'ms', 'dr', name='Salutation'), nullable=True),
    sa.Column('first_name', sa.String(length=100), nullable=False),
    sa.Column('last_name', sa.String(length=100), nullable=False),
    sa.Column('phone_primary', sa.String(length=25), nullable=True),
    sa.Column('gender', sa.Enum('female', 'male', 'non_binary', name='Gender'), nullable=True),
    sa.Column('race_all', sa.Enum('asian', 'white', 'black', 'hispanic', name='Race'), nullable=True),
    sa.Column('birthdate', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('type', sa.Enum('function', 'skill', 'topic', name='TagType'), nullable=False),
    sa.Column('status', sa.Enum('active', 'inactive', name='TagStatusType'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('address',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('contact_id', sa.Integer(), nullable=False),
    sa.Column('is_primary', sa.Boolean(), nullable=True),
    sa.Column('street1', sa.String(length=200), nullable=False),
    sa.Column('street2', sa.String(length=200), nullable=True),
    sa.Column('city', sa.String(length=100), nullable=False),
    sa.Column('state', sa.String(length=100), nullable=False),
    sa.Column('country', sa.String(length=100), nullable=False),
    sa.Column('postal_code', sa.String(length=10), nullable=False),
    sa.Column('type', sa.Enum('home', 'work', name='AddressType'), nullable=True),
    sa.Column('status', sa.Enum('active', 'inactive', name='Status'), nullable=True),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('email',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('contact_id', sa.Integer(), nullable=False),
    sa.Column('is_primary', sa.Boolean(), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('type', sa.Enum('personal', 'work', name='EmailType'), nullable=True),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('resume',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('contact_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('date_created', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tag_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('contact_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('experience',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('host', sa.String(length=100), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('degree', sa.Enum('high_school', 'associates', 'undergraduate', 'masters', 'doctoral', name='Degree'), nullable=True),
    sa.Column('date_start', sa.Date(), nullable=False),
    sa.Column('date_end', sa.Date(), nullable=True),
    sa.Column('type', sa.Enum('work', 'service', 'accomplishment', 'education', name='ExperienceType'), nullable=True),
    sa.Column('contact_id', sa.Integer(), nullable=False),
    sa.Column('address_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['address_id'], ['address.id'], ),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('resume_section',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('resume_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('min_count', sa.Integer(), nullable=True),
    sa.Column('max_count', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['resume_id'], ['resume.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('achievement',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('exp_id', sa.Integer(), nullable=False),
    sa.Column('contact_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.ForeignKeyConstraint(['exp_id'], ['experience.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('resume_item',
    sa.Column('resume_order', sa.Integer(), nullable=False),
    sa.Column('section_id', sa.Integer(), nullable=False),
    sa.Column('exp_id', sa.Integer(), nullable=True),
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.Column('achievement_id', sa.Integer(), nullable=True),
    sa.Column('resume_id', sa.Integer(), nullable=True),
    sa.Column('indented', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['achievement_id'], ['achievement.id'], ),
    sa.ForeignKeyConstraint(['exp_id'], ['experience.id'], ),
    sa.ForeignKeyConstraint(['resume_id'], ['resume.id'], ),
    sa.ForeignKeyConstraint(['section_id'], ['resume_section.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag_item.id'], ),
    sa.PrimaryKeyConstraint('resume_order', 'section_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('resume_item')
    op.drop_table('achievement')
    op.drop_table('resume_section')
    op.drop_table('experience')
    op.drop_table('tag_item')
    op.drop_table('resume')
    op.drop_table('email')
    op.drop_table('address')
    op.drop_table('tag')
    op.drop_table('contact')
    # ### end Alembic commands ###
