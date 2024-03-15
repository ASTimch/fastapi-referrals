"""refactor without fastapi_users

Revision ID: 003
Revises: 002
Create Date: 2024-03-15 00:32:30.326861

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user", "is_superuser")
    op.drop_column("user", "is_verified")
    op.drop_column("user", "is_active")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user",
        sa.Column(
            "is_active", sa.BOOLEAN(), autoincrement=False, nullable=False
        ),
    )
    op.add_column(
        "user",
        sa.Column(
            "is_verified", sa.BOOLEAN(), autoincrement=False, nullable=False
        ),
    )
    op.add_column(
        "user",
        sa.Column(
            "is_superuser", sa.BOOLEAN(), autoincrement=False, nullable=False
        ),
    )
    # ### end Alembic commands ###
