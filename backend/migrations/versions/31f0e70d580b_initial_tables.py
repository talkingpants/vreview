"""initial tables

Revision ID: 31f0e70d580b
Revises: 
Create Date: 2025-06-26

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '31f0e70d580b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'vulnerabilities',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('defender_id', sa.String(length=50), nullable=False, unique=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('severity', sa.String(length=20)),
        sa.Column('discovered_at', sa.DateTime()),
    )
    op.create_table(
        'reviews',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('vulnerability_id', sa.Integer(), sa.ForeignKey('vulnerabilities.id'), nullable=False),
        sa.Column('status', sa.String(length=50), default='pending'),
        sa.Column('comments', sa.Text()),
        sa.Column('reviewed_at', sa.DateTime()),
    )
    op.create_table(
        'tickets',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('review_id', sa.Integer(), sa.ForeignKey('reviews.id'), nullable=False),
        sa.Column('ticket_number', sa.String(length=50), unique=True),
        sa.Column('status', sa.String(length=50), default='open'),
        sa.Column('created_at', sa.DateTime()),
    )


def downgrade():
    op.drop_table('tickets')
    op.drop_table('reviews')
    op.drop_table('vulnerabilities')
