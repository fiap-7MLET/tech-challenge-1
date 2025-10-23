"""add auth fields to user model

Revision ID: 6995c20bc64c
Revises: b75f99e2b181
Create Date: 2025-10-22 23:32:57.719317

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6995c20bc64c'
down_revision: Union[str, Sequence[str], None] = 'b75f99e2b181'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add new columns to users table
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'))
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=False, server_default='0'))
    op.add_column('users', sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()))

    # Add indexes for better query performance
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # Increase password column length for bcrypt hashes
    with op.batch_alter_table('users') as batch_op:
        batch_op.alter_column('password',
                   existing_type=sa.String(length=128),
                   type_=sa.String(length=255),
                   existing_nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Drop indexes
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')

    # Remove columns
    op.drop_column('users', 'created_at')
    op.drop_column('users', 'is_admin')
    op.drop_column('users', 'is_active')

    # Revert password column length
    with op.batch_alter_table('users') as batch_op:
        batch_op.alter_column('password',
                   existing_type=sa.String(length=255),
                   type_=sa.String(length=128),
                   existing_nullable=False)
