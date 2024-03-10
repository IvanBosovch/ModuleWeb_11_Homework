"""'Init'

Revision ID: 4f54ae540319
Revises: af702ca48ea3
Create Date: 2024-03-03 14:14:20.635521

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4f54ae540319'
down_revision: Union[str, None] = 'af702ca48ea3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users_login', sa.Column('confirmed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users_login', 'confirmed')
    # ### end Alembic commands ###