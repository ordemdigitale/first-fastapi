"""add content column to posts table

Revision ID: 6183255dd8e4
Revises: e674c1cf490b
Create Date: 2023-10-26 23:05:47.155198

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6183255dd8e4'
down_revision: Union[str, None] = 'e674c1cf490b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("content", sa.String(), nullable=False)
    )


def downgrade() -> None:
    op.drop_column(
        "posts",
        "content"
    )
