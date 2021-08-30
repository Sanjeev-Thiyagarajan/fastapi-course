"""add content column to posts table

Revision ID: 01b2584928a5
Revises: cfcc4fd02d18
Create Date: 2021-08-29 22:59:51.536022

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01b2584928a5'
down_revision = 'cfcc4fd02d18'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
