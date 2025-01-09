"""Initial migration for users, transactions, and admins tables

Revision ID: f7031c72249f
Revises: 
Create Date: 2025-01-09 00:44:09.025658

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'f7031c72249f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admins',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_admins_id'), 'admins', ['id'], unique=False)
    op.drop_table('transactions')
    op.alter_column('users', 'email',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.create_index(op.f('ix_users_user_id'), 'users', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_user_id'), table_name='users')
    op.alter_column('users', 'email',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.create_table('transactions',
    sa.Column('transaction_id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('trans_date', mysql.TIMESTAMP(), nullable=False),
    sa.Column('cc_num', mysql.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('merchant', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('category', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('amount', mysql.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('city', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('state', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('zip_code', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('job', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('trans_num', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('merch_lat', mysql.DECIMAL(precision=10, scale=6), nullable=True),
    sa.Column('merch_long', mysql.DECIMAL(precision=10, scale=6), nullable=True),
    sa.Column('is_fraud', mysql.TINYINT(display_width=1), server_default=sa.text("'0'"), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name='transactions_ibfk_1'),
    sa.PrimaryKeyConstraint('transaction_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_index(op.f('ix_admins_id'), table_name='admins')
    op.drop_table('admins')
    # ### end Alembic commands ###
