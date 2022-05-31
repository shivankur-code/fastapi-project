"""create content coloumn in posts table

Revision ID: ccb86452fba7
Revises: 3c81a84b5394
Create Date: 2022-05-30 12:11:30.669409

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ccb86452fba7'
down_revision = '3c81a84b5394'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable = False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
