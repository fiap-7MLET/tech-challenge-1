"""add scraping_jobs table

Revision ID: 0671e50f7a9a
Revises: b75f99e2b181
Create Date: 2025-11-02 20:15:54.457500

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0671e50f7a9a'
down_revision: Union[str, Sequence[str], None] = 'b75f99e2b181'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'scraping_jobs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('started_at', sa.DateTime(), nullable=False),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('books_scraped', sa.Integer(), nullable=True),
        sa.Column('books_saved', sa.Integer(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('csv_file', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('scraping_jobs')
