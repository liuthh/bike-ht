"""empty message

Revision ID: d66c6374d0a4
Revises: e908e7cf2eab
Create Date: 2018-11-01 12:25:57.440098

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd66c6374d0a4'
down_revision = 'e908e7cf2eab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('rcaddress', 'user_id',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)
    op.drop_constraint('rcaddress_ibfk_1', 'rcaddress', type_='foreignkey')
    op.create_foreign_key(None, 'rcaddress', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'rcaddress', type_='foreignkey')
    op.create_foreign_key('rcaddress_ibfk_1', 'rcaddress', 'user', ['user_id'], ['id'])
    op.alter_column('rcaddress', 'user_id',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)
    # ### end Alembic commands ###