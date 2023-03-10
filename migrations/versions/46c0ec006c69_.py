"""empty message

Revision ID: 46c0ec006c69
Revises: b3c307b36e00
Create Date: 2023-02-12 00:10:24.326107

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46c0ec006c69'
down_revision = 'b3c307b36e00'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('barcode', sa.String(length=20), nullable=True))
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=200),
               type_=sa.String(length=100),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=200),
               existing_nullable=True)
        batch_op.drop_column('barcode')

    # ### end Alembic commands ###
