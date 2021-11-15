"""content column

Revision ID: 7ee5c52ab67e
Revises: ef96d0f11468
Create Date: 2021-11-14 13:31:17.459136

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ee5c52ab67e'
down_revision = 'ef96d0f11468'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts",sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("posts","content")
    pass
