"""empty message

Revision ID: 6dd26ec7c93e
Revises: 4be84846d62e
Create Date: 2019-11-25 15:59:35.290206

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6dd26ec7c93e'
down_revision = '4be84846d62e'
branch_labels = None
depends_on = None

old_options = ('associates', 'undergraduate','masters', 'doctoral')
new_options = (('classes', 'training', 'certificate', 'ged', 'high_school')
                + old_options + ('other',))

old_type = sa.Enum(*old_options, name='Degree')
new_type = sa.Enum(*new_options, name='Degree')

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('experience', sa.Column('degree_other', sa.String(length=100), nullable=True))
    # Drop the "old" "Degree" enum
    old_type.drop(op.get_bind(), checkfirst=False)
    # Create the "new" "MonthType" enum with the same name as the old type
    new_type.create(op.get_bind(), checkfirst=False)
    op.alter_column('experience', 'degree', type_=new_type,
                    existing_type=sa.String(length=100), postgresql_using='degree::"Degree"')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('experience', 'degree_other')
    # Drop the "Degree" enum with the "new" values
    op.alter_column('experience', 'degree', type_=sa.String(length=100), existing_type=new_type)
    new_type.drop(op.get_bind(), checkfirst=False)
    # Create the "new" "Degree" enum with the original values
    old_type.create(op.get_bind(), checkfirst=False)
    # ### end Alembic commands ###
