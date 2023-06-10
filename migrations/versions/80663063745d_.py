"""empty message

Revision ID: 80663063745d
Revises: 
Create Date: 2023-06-10 00:08:55.409299

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80663063745d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('coupons',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('code', sa.String(length=50), nullable=True),
    sa.Column('percentage', sa.Float(precision=2), nullable=True),
    sa.Column('started_at', sa.DateTime(), nullable=True),
    sa.Column('ended_at', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code')
    )
    op.create_table('plans',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('price', sa.Float(precision=2), nullable=True),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.Column('mercadopago_id', sa.String(length=50), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('last_name', sa.String(length=120), nullable=True),
    sa.Column('username', sa.String(length=80), nullable=True),
    sa.Column('password', sa.String(length=120), nullable=False),
    sa.Column('email', sa.String(length=140), nullable=True),
    sa.Column('rol_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('token', sa.String(length=20), nullable=True),
    sa.Column('avatar', sa.String(length=80), nullable=True),
    sa.Column('fb_id', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['rol_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('total_price', sa.Float(precision=2), nullable=True),
    sa.Column('subtotal_price', sa.Float(precision=2), nullable=True),
    sa.Column('discount_price', sa.Float(precision=2), nullable=True),
    sa.Column('code_coupon', sa.String(length=50), nullable=True),
    sa.Column('date_create', sa.Date(), nullable=True),
    sa.Column('checkout_id', sa.String(length=255), nullable=True),
    sa.Column('checkout_url', sa.String(length=255), nullable=True),
    sa.Column('payment_status', sa.String(length=255), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('plan_id', sa.Integer(), nullable=True),
    sa.Column('subscription_id', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['plan_id'], ['plans.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('products',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('image', sa.String(length=255), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('unit', sa.String(length=40), nullable=True),
    sa.Column('spoilDate', sa.DateTime(), nullable=True),
    sa.Column('barcode', sa.String(length=20), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('subscriptions',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('mercadopago_subscription_id', sa.String(length=50), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favorites',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favorites')
    op.drop_table('subscriptions')
    op.drop_table('products')
    op.drop_table('orders')
    op.drop_table('users')
    op.drop_table('roles')
    op.drop_table('plans')
    op.drop_table('coupons')
    op.drop_table('categories')
    # ### end Alembic commands ###
