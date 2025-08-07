"""add supplement models

Revision ID: 8f5a2c3d1e9b
Revises: 7e67e11cd488
Create Date: 2023-08-05 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f5a2c3d1e9b'
down_revision = '7e67e11cd488'
branch_labels = None
depends_on = None


def upgrade():
    # Create supplements table
    op.create_table('supplements',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('dosage', sa.String(length=50), nullable=True),
        sa.Column('stock_level', sa.Integer(), nullable=True),
        sa.Column('low_stock_threshold', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create supplement_intakes table
    op.create_table('supplement_intakes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('supplement_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('family_member_id', sa.Integer(), nullable=True),
        sa.Column('taken_at', sa.DateTime(), nullable=True),
        sa.Column('dosage_taken', sa.String(length=50), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('photo_confirmation', sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(['family_member_id'], ['family_members.id'], ),
        sa.ForeignKeyConstraint(['supplement_id'], ['supplements.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create reminders table
    op.create_table('reminders',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('supplement_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('family_member_id', sa.Integer(), nullable=True),
        sa.Column('time', sa.Time(), nullable=False),
        sa.Column('days', sa.String(length=50), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['family_member_id'], ['family_members.id'], ),
        sa.ForeignKeyConstraint(['supplement_id'], ['supplements.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('reminders')
    op.drop_table('supplement_intakes')
    op.drop_table('supplements')