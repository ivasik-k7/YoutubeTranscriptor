"""Make resource address unique

Revision ID: bc19335e7b42
Revises: bf4f544f079e
Create Date: 2024-06-02 22:20:41.696937

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "bc19335e7b42"
down_revision: Union[str, None] = "bf4f544f079e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, "streaming_resources", ["url"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "streaming_resources", type_="unique")
    # ### end Alembic commands ###
