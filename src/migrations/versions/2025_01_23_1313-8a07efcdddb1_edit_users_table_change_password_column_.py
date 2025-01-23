"""edit users table, change  password column to hashed_password, add first_name, last_name

Revision ID: 8a07efcdddb1
Revises: 06717354de51
Create Date: 2025-01-23 13:13:37.593672

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8a07efcdddb1"
down_revision: Union[str, None] = "06717354de51"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users", sa.Column("first_name", sa.String(length=50), nullable=False)
    )
    op.add_column(
        "users", sa.Column("last_name", sa.String(length=100), nullable=False)
    )
    op.add_column(
        "users", sa.Column("hashed_password", sa.String(length=200), nullable=False)
    )
    op.drop_column("users", "password")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users",
        sa.Column(
            "password", sa.VARCHAR(length=200), autoincrement=False, nullable=False
        ),
    )
    op.drop_column("users", "hashed_password")
    op.drop_column("users", "last_name")
    op.drop_column("users", "first_name")
    # ### end Alembic commands ###
