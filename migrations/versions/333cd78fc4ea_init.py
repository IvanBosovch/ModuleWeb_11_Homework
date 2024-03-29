"""'Init'

Revision ID: 333cd78fc4ea
Revises: c685f73256b9
Create Date: 2024-02-26 18:19:25.828670

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '333cd78fc4ea'
down_revision: Union[str, None] = 'c685f73256b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'phone',
               existing_type=sa.VARCHAR(length=11),
               type_=sa.String(length=20),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'phone',
               existing_type=sa.String(length=20),
               type_=sa.VARCHAR(length=11),
               existing_nullable=True)
    # ### end Alembic commands ###
