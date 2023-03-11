"""plan update field

Revision ID: ea236ce0aca8
Revises: 6e6a69518d9d
Create Date: 2023-03-10 17:16:04.610403

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea236ce0aca8'
down_revision = '6e6a69518d9d'
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
        batch_op.alter_column('mercadopago_id',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=50),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('plans', schema=None) as batch_op:
        batch_op.alter_column('mercadopago_id',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=20),
               existing_nullable=True)
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