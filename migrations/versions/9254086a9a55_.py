"""empty message

Revision ID: 9254086a9a55
Revises: 80663063745d
Create Date: 2023-06-10 01:23:52.802761

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9254086a9a55'
down_revision = '80663063745d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('coupons', schema=None) as batch_op:
        batch_op.alter_column('percentage',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=True)

    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.alter_column('total_price',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=True)
        batch_op.alter_column('subtotal_price',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=True)
        batch_op.alter_column('discount_price',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=True)

    with op.batch_alter_table('plans', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=True)

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('avatar',
               existing_type=sa.VARCHAR(length=80),
               type_=sa.String(length=100),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('avatar',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=80),
               existing_nullable=True)

    with op.batch_alter_table('plans', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=True)

    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.alter_column('discount_price',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=True)
        batch_op.alter_column('subtotal_price',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=True)
        batch_op.alter_column('total_price',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=True)

    with op.batch_alter_table('coupons', schema=None) as batch_op:
        batch_op.alter_column('percentage',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=True)

    # ### end Alembic commands ###