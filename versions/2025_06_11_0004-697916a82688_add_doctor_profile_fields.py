"""add doctor profile fields

Revision ID: 697916a82688
Revises: b515bbfab9e1
Create Date: 2025-06-11 00:04:31.025047

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '697916a82688'
down_revision: Union[str, None] = 'b515bbfab9e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    from sqlalchemy.dialects import postgresql
    op.add_column('doctors', sa.Column('certifications', sa.String(), nullable=True))
    op.add_column('doctors', sa.Column('languages_spoken', postgresql.ARRAY(sa.String()), nullable=True))
    op.add_column('doctors', sa.Column('fees', sa.Float(), nullable=True))
    op.add_column('doctors', sa.Column('insurance_accepted', sa.Integer(), nullable=True))
    op.add_column('doctors', sa.Column('areas_of_expertise', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('doctors', 'areas_of_expertise')
    op.drop_column('doctors', 'insurance_accepted')
    op.drop_column('doctors', 'fees')
    op.drop_column('doctors', 'languages_spoken')
    op.drop_column('doctors', 'certifications')
    # ### end Alembic commands ###
