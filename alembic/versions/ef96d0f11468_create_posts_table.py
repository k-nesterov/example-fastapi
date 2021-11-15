"""create posts table

Revision ID: ef96d0f11468
Revises: 
Create Date: 2021-11-14 13:21:49.156911

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef96d0f11468'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # create table
    op.create_table("posts",
                    sa.Column("id", sa.INTEGER, nullable=False, primary_key=True),
                    sa.Column("title", sa.String, nullable=False))
    pass


def downgrade():
    op.drop_table("posts")
    pass
