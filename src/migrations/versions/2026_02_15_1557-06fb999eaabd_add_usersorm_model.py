"""add UsersORM model

Revision ID: 06fb999eaabd
Revises: e7df59088151
Create Date: 2026-02-15 15:57:18.360656

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "06fb999eaabd"
down_revision: Union[str, Sequence[str], None] = "e7df59088151"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
