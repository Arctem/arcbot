"""Add bot column to user.

Revision ID: ce6d93384745
Revises:
Create Date: 2016-08-09 22:01:19.171177

"""

# revision identifiers, used by Alembic.
revision = 'ce6d93384745'
down_revision = None
branch_labels = None
depends_on = None

import sqlalchemy as sa

from alembic import op


def upgrade():
    op.add_column('users', sa.Column('bot', sa.Boolean, default=False))


def downgrade():
    op.drop_column('users', 'bot')
