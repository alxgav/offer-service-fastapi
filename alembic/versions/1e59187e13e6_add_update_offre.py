"""add update offre

Revision ID: 1e59187e13e6
Revises: 
Create Date: 2025-01-04 14:35:00.453851

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1e59187e13e6"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "offers",
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("image", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        schema="offer",
    )
    op.create_table(
        "offer_options",
        sa.Column("offer_id", sa.UUID(), nullable=False),
        sa.Column("is_temporary", sa.Boolean(), nullable=False),
        sa.Column("temporary_to", sa.DateTime(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["offer_id"],
            ["offer.offers.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="offer",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("offer_options", schema="offer")
    op.drop_table("offers", schema="offer")
    # ### end Alembic commands ###
