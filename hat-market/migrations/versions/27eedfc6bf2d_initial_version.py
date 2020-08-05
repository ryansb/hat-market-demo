"""Initial version

Revision ID: 27eedfc6bf2d
Revises:
Create Date: 2020-08-02 14:22:44.779624

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27eedfc6bf2d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    '''Our first data model'''
    op.execute("CREATE SEQUENCE IF NOT EXISTS hat_upc_seq;")
    op.create_table(
        "hat",
        sa.Column(
            "upc",
            sa.Integer(),
            server_default=sa.text("nextval('hat_upc_seq'::regclass)"),
            nullable=False,
        ),
        sa.Column("capacity", sa.String(length=127), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("stock", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("upc"),
    )
    # op.add_column('hat', sa.Column('image_link', sa.Text(), nullable=True))
    # op.drop_column('hat', 'image_link')


def downgrade():
    '''remove our only table'''
    op.drop_table('hat')
    op.execute("DROP SEQUENCE IF EXISTS hat_upc_seq;")
