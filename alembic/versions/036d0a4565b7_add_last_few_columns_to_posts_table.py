"""add last few columns to posts table

Revision ID: 036d0a4565b7
Revises: af786b740296
Create Date: 2021-08-29 23:14:45.193298

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '036d0a4565b7'
down_revision = 'af786b740296'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
