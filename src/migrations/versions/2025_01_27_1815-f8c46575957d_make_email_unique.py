"""make email unique

Revision ID: f8c46575957d
Revises: 8a07efcdddb1
Create Date: 2025-01-27 18:15:28.718838

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f8c46575957d"
down_revision: Union[str, None] = "8a07efcdddb1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])



def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")

