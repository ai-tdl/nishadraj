"""finalize auth_002 institutional

Revision ID: cf38d4a4928d
Revises: a11d8eca77bc
Create Date: 2026-02-25 14:23:47.178817

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cf38d4a4928d'
down_revision: Union[str, Sequence[str], None] = 'a11d8eca77bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Add account_locked to users
    op.add_column('users', sa.Column('account_locked', sa.Boolean(), nullable=False, server_default=sa.text('false')))

    # 2. Refactor audit_logs table
    op.add_column('audit_logs', sa.Column('module', sa.String(length=100), nullable=False, server_default='AUTH'))
    op.add_column('audit_logs', sa.Column('description', sa.String(length=255), nullable=False, server_default='No description'))
    
    # Rename created_at to timestamp
    op.alter_column('audit_logs', 'created_at', new_column_name='timestamp')
    
    # Remove old fields to match Phase 6 specification
    op.drop_column('audit_logs', 'resource')
    op.drop_column('audit_logs', 'status')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('audit_logs', sa.Column('status', sa.String(length=50), nullable=True))
    op.add_column('audit_logs', sa.Column('resource', sa.String(length=255), nullable=True))
    op.alter_column('audit_logs', 'timestamp', new_column_name='created_at')
    op.drop_column('audit_logs', 'description')
    op.drop_column('audit_logs', 'module')
    op.drop_column('users', 'account_locked')
