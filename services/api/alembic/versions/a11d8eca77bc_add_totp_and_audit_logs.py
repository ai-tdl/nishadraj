"""add totp and audit logs

Revision ID: a11d8eca77bc
Revises: f3902bb17ca2
Create Date: 2026-02-25 14:05:26.558720

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a11d8eca77bc'
down_revision: Union[str, Sequence[str], None] = 'f3902bb17ca2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

from sqlalchemy.dialects import postgresql

def upgrade() -> None:
    """Upgrade schema."""
    # Add columns to users table
    op.add_column('users', sa.Column('totp_secret', sa.String(length=32), nullable=True))
    op.add_column('users', sa.Column('is_2fa_enabled', sa.Boolean(), nullable=False, server_default=sa.text('false')))
    op.add_column('users', sa.Column('failed_login_attempts', sa.Integer(), nullable=False, server_default=sa.text('0')))
    op.add_column('users', sa.Column('last_login_at', sa.DateTime(), nullable=True))

    # Create audit_logs table
    op.create_table(
        'audit_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('event_type', sa.String(length=100), nullable=False),
        sa.Column('resource', sa.String(length=255), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('details', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('audit_logs')
    op.drop_column('users', 'last_login_at')
    op.drop_column('users', 'failed_login_attempts')
    op.drop_column('users', 'is_2fa_enabled')
    op.drop_column('users', 'totp_secret')
