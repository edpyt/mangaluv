"""add unique user email field

Revision ID: 27f4d4145895
Revises: 55b63818f08b
Create Date: 2025-08-02 17:27:31.791012

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "27f4d4145895"
down_revision: str | Sequence[str] | None = "55b63818f08b"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("email", sa.String(), nullable=False))
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_column("users", "email")
    # ### end Alembic commands ###
