"""create relation posts-users

Revision ID: 21f0fe33b375
Revises: ee7969394dd4
Create Date: 2021-11-14 14:58:20.563143

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21f0fe33b375'
down_revision = 'ee7969394dd4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key("posts_users_fkey", source_table="posts",
                          referent_table="users", local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('posts_users_fkey', table_name="posts")
    op.drop_column("posts","owner_id")
    pass
