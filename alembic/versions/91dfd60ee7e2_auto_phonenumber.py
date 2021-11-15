"""auto-phonenumber

Revision ID: 91dfd60ee7e2
Revises: 6fd305914c43
Create Date: 2021-11-14 15:49:38.980110

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91dfd60ee7e2'
down_revision = '6fd305914c43'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_number')
    # ### end Alembic commands ###