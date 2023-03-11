"""plan update

Revision ID: 6e6a69518d9d
Revises: ab151fa98c8f
Create Date: 2023-03-10 17:09:35.753727

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e6a69518d9d'
down_revision = 'ab151fa98c8f'
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
        batch_op.drop_column('igv_price')

    with op.batch_alter_table('plans', schema=None) as batch_op:
        batch_op.add_column(sa.Column('mercadopago_id', sa.String(length=20), nullable=True))
        batch_op.alter_column('price',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('plans', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=True)
        batch_op.drop_column('mercadopago_id')

    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('igv_price', sa.REAL(), autoincrement=False, nullable=True))
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
