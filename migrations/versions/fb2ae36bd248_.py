"""empty message

Revision ID: fb2ae36bd248
Revises: 51f4efa89e84
Create Date: 2019-10-11 15:11:41.589363

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'fb2ae36bd248'
down_revision = '51f4efa89e84'
branch_labels = None
depends_on = None

old_options = ('january', 'february', 'march', 'april', 'may', 'june', 'july',
               'august', 'september', 'october', 'november', 'december')
new_options = ('none',) + old_options

old_type = sa.Enum(*old_options, name='MonthType')
new_type = sa.Enum(*new_options, name='MonthType')
tmp_type = sa.Enum(*new_options, name='_MonthType')

def upgrade():
    '''
    Explantion for this migration script can be found on this stack exchange
    question: https://stackoverflow.com/questions/14845203/altering-an-enum-field-using-alembic
    '''
    # Create a tempoary "_MonthType" enum with the new values
    tmp_type.create(op.get_bind(), checkfirst=False)
    # Converts the columns from the old "MonthType" to the temp "_MonthType"
    op.execute('ALTER TABLE Experience ALTER COLUMN end_month '
               'TYPE "_MonthType" USING end_month::text::"_MonthType"')
    op.execute('ALTER TABLE Experience ALTER COLUMN start_month '
               'TYPE "_MonthType" USING start_month::text::"_MonthType"')
    #drops the old enum so we can create the new enum with the same name
    old_type.drop(op.get_bind(), checkfirst=False)
    # Create the "new" "MonthType" enum with the same name as the old type
    new_type.create(op.get_bind(), checkfirst=False)
    # Replaces the temp enum with the correctly named new enum
    op.execute('ALTER TABLE Experience ALTER COLUMN end_month '
               'TYPE "MonthType" USING end_month::text::"MonthType"')
    op.execute('ALTER TABLE Experience ALTER COLUMN start_month '
               'TYPE "MonthType" USING start_month::text::"MonthType"')
    # Drops the temp enum
    tmp_type.drop(op.get_bind(), checkfirst=False)

    #Makes the other changes to the columns
    op.alter_column('experience', 'end_month',
               existing_type=new_type,
               nullable=False)
    op.alter_column('experience', 'end_year',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('experience', 'start_month',
               existing_type=new_type,
               nullable=False)
    # ### end Alembic commands ###


def downgrade():

    # makes the other changes to the columns
    op.alter_column('experience', 'start_month',
               existing_type=new_type,
               nullable=True)
    op.alter_column('experience', 'end_year',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('experience', 'end_month',
               existing_type=new_type,
               nullable=True)

    # Create a tempoary "_MonthType" enum with the new values
    tmp_type.create(op.get_bind(), checkfirst=False)
    # Replaces the new "MonthType" with the temp "_MonthType"
    op.execute('ALTER TABLE Experience ALTER COLUMN end_month '
               'TYPE "_MonthType" USING end_month::text::"_MonthType"')
    op.execute('ALTER TABLE Experience ALTER COLUMN start_month '
               'TYPE "_MonthType" USING start_month::text::"_MonthType"')
    # Drops the "new" "MonthType" enum with the same name as the old type
    new_type.drop(op.get_bind(), checkfirst=False)
    # Creates the "old" "MonthType" enum with the same name as the "new" enum
    old_type.create(op.get_bind(), checkfirst=False)
    # Replaces the temp enum with the "old" enum
    op.execute('ALTER TABLE Experience ALTER COLUMN end_month '
               'TYPE "MonthType" USING end_month::text::"MonthType"')
    op.execute('ALTER TABLE Experience ALTER COLUMN start_month '
               'TYPE "MonthType" USING start_month::text::"MonthType"')
    # Drops the temp enum
    tmp_type.drop(op.get_bind(), checkfirst=False)
