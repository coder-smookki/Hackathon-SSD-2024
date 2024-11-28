"""empty message

Revision ID: 0002
Revises: 0001
Create Date: 2024-11-28 02:28:19.570318

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0002'
down_revision: Union[str, None] = '0001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('tg_id', sa.BigInteger(), nullable=False),
    sa.Column('login', sa.String(length=128), nullable=False),
    sa.Column('email', sa.String(length=254), nullable=False),
    sa.Column('token', sa.String(length=4000), nullable=False),
    sa.Column('token_expired_at', sa.DateTime(), nullable=False),
    sa.Column('refresh_token', sa.String(length=1000), nullable=False),
    sa.Column('refresh_token_expired_at', sa.DateTime(), nullable=False),
    sa.Column('events', sa.ARRAY(sa.Integer()), nullable=True),
    sa.Column('vcc_id', sa.BigInteger(), nullable=False),
    sa.Column('first_name', sa.String(length=64), nullable=False),
    sa.Column('last_name', sa.String(length=64), nullable=False),
    sa.Column('midle_name', sa.String(length=64), nullable=True),
    sa.Column('birthday', sa.Date(), nullable=True),
    sa.Column('phone', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('tg_id', name=op.f('pk_users'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
