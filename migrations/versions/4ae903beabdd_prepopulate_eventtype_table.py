"""Prepopulate eventtype table

Revision ID: 4ae903beabdd
Revises: c1df5df90044
Create Date: 2023-04-19 23:21:01.924442

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String


# revision identifiers, used by Alembic.
revision = '4ae903beabdd'
down_revision = 'c1df5df90044'
branch_labels = None
depends_on = None


def upgrade():
    # Create a reference to the eventtype table
    eventtype_table = table('event_type',
        column('name', String)
    )

    # Insert multiple event types into the eventtype table
    op.bulk_insert(eventtype_table, [
        {'name': 'birthday'},
        {'name': 'medical appointment'},
        {'name': 'vacation'},
        {'name': 'work'},
    ])


def downgrade():
    # Remove the specified event types from the eventtype table
    op.execute("DELETE FROM event_type WHERE name IN ('birthday', 'medical appointment', 'vacation', 'work')")
