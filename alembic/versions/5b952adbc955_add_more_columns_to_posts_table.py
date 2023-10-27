"""add more columns to posts table

Revision ID: 5b952adbc955
Revises: 55b2f81c1341
Create Date: 2023-10-26 23:29:52.026870

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b952adbc955'
down_revision: Union[str, None] = '55b2f81c1341'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published", sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),)


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
