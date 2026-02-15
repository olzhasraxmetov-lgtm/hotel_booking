"""add unique parametr for email

Revision ID: 2a18d4b64236
Revises: 06fb999eaabd
Create Date: 2026-02-15 17:17:13.045546

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "2a18d4b64236"
down_revision: Union[str, Sequence[str], None] = "06fb999eaabd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "users", type_="unique")
