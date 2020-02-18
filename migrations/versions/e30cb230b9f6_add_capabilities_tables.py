"""Add capabilities tables

Revision ID: e30cb230b9f6
Revises: 8d25b12fb35b
Create Date: 2020-02-18 14:54:11.742884

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e30cb230b9f6'
down_revision = '8d25b12fb35b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('capability',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name', name='capability_name_uniq')
    )
    op.create_table('skill',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name', name='skill_name_uniq')
    )
    op.create_table('capability_skill_recommendations',
    sa.Column('capability_id', sa.String(), nullable=False),
    sa.Column('skill_id', sa.String(), nullable=False),
    sa.Column('order', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['capability_id'], ['capability.id'], ),
    sa.ForeignKeyConstraint(['skill_id'], ['skill.id'], ),
    sa.PrimaryKeyConstraint('capability_id', 'skill_id', name='cap_skill_rec_pk'),
    sa.UniqueConstraint('capability_id', 'order', name='cap_skill_rec_order_uniq')
    )
    op.create_table('capability_skill_suggestions',
    sa.Column('capability_id', sa.String(), nullable=False),
    sa.Column('skill_id', sa.String(), nullable=False),
    sa.Column('contact_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['capability_id'], ['capability.id'], ),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.ForeignKeyConstraint(['skill_id'], ['skill.id'], ),
    sa.PrimaryKeyConstraint('contact_id', 'capability_id', 'skill_id', name='cap_skill_suggestion_pk')
    )
    op.create_table('capability_skills',
    sa.Column('capability_id', sa.String(), nullable=False),
    sa.Column('skill_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['capability_id'], ['capability.id'], ),
    sa.ForeignKeyConstraint(['skill_id'], ['skill.id'], ),
    sa.PrimaryKeyConstraint('capability_id', 'skill_id', name='capability_skills_pk')
    )
    op.create_table('contact_skill_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('skill_id', sa.String(), nullable=True),
    sa.Column('contact_id', sa.Integer(), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.ForeignKeyConstraint(['skill_id'], ['skill.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('experience_skill_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('experience_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['experience_id'], ['experience.id'], ),
    sa.ForeignKeyConstraint(['parent_id'], ['contact_skill_item.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('achievement_skill_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('achievement_id', sa.Integer(), nullable=True),
    sa.Column('capability_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['achievement_id'], ['achievement.id'], ),
    sa.ForeignKeyConstraint(['capability_id'], ['capability.id'], ),
    sa.ForeignKeyConstraint(['parent_id'], ['experience_skill_item.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('achievement_skill_item')
    op.drop_table('experience_skill_item')
    op.drop_table('contact_skill_item')
    op.drop_table('capability_skills')
    op.drop_table('capability_skill_suggestions')
    op.drop_table('capability_skill_recommendations')
    op.drop_table('skill')
    op.drop_table('capability')
    # ### end Alembic commands ###
