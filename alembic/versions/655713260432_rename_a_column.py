"""Rename a column.

Revision ID: 655713260432
Revises: ce6d93384745
Create Date: 2018-02-04 23:34:26.968013

"""

# revision identifiers, used by Alembic.
revision = '655713260432'
down_revision = 'ce6d93384745'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('user_channel', sa.Column('user_id', sa.Integer))


def downgrade():
    op.drop_column('user_channel', 'user_id')
