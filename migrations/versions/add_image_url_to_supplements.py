"""add image_url to supplements

Revision ID: 9f6b3d4e2f0c
Revises: 8f5a2c3d1e9b
Create Date: 2023-08-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f6b3d4e2f0c'
down_revision = '8f5a2c3d1e9b'
branch_labels = None
depends_on = None


def upgrade():
    # Add image_url column to supplements table
    op.add_column('supplements', sa.Column('image_url', sa.String(length=255), nullable=True))


def downgrade():
    # Remove image_url column from supplements table
    op.drop_column('supplements', 'image_url')