"""add columnt to post

Revision ID: 8452d4bc332a
Revises: 21f0fe33b375
Create Date: 2021-11-14 15:14:08.699581

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8452d4bc332a'
down_revision = '21f0fe33b375'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("published", sa.Boolean(),
                  nullable=False, server_default='TRUE'))
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                  nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
