"""initial migration

Revision ID: 980836b3cc56
Revises: a46abf5bda7e
Create Date: 2025-01-14 17:28:12.399554

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '980836b3cc56'
down_revision: Union[str, None] = 'a46abf5bda7e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("rooms",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id")
    )


def downgrade() -> None:
    op.drop_table("rooms")
