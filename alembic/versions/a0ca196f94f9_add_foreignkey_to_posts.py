"""add foreignkey to posts

Revision ID: a0ca196f94f9
Revises: 132cd46d28b1
Create Date: 2022-05-30 13:21:55.713708

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0ca196f94f9'
down_revision = '132cd46d28b1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable = False))
    op.create_foreign_key('posts_user_fk', source_table = 'posts', referent_table = 'users', local_cols = ['owner_id'], remote_cols = ['id'], ondelete = 'CASCADE')
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
