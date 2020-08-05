"""add images to the API

Revision ID: b84c195d2e6a
Revises: 27eedfc6bf2d
Create Date: 2020-08-05 10:29:57.411976

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b84c195d2e6a'
down_revision = '27eedfc6bf2d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('hat', sa.Column('image_link', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('hat', 'image_link')
