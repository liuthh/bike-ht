"""empty message

Revision ID: c92778f6856b
Revises: 765366de103b
Create Date: 2018-10-29 10:45:56.562872

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c92778f6856b'
down_revision = '765366de103b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('cart', 'goods_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('cart', 'number',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('cart', 'number',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('cart', 'goods_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    # ### end Alembic commands ###
