"""add championships table

Revision ID: 103a684b2891
Revises: 409595b2e9e6
Create Date: 2024-09-07 01:41:03.155123

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '103a684b2891'
down_revision: Union[str, None] = '409595b2e9e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('championships',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('format', sa.String(), nullable=False),
    sa.Column('context', sa.String(), nullable=False),
    sa.Column('country', sa.String(), nullable=False),
    sa.Column('start_year', sa.Integer(), nullable=False),
    sa.Column('end_year', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('championships')
    # ### end Alembic commands ###
