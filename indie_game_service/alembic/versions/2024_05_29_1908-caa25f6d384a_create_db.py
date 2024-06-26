"""create db

Revision ID: caa25f6d384a
Revises: 
Create Date: 2024-05-29 19:08:36.996669

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'caa25f6d384a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('date_create', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_posts')),
    sa.UniqueConstraint('name', name=op.f('uq_posts_name'))
    )
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('date_create', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], name=op.f('fk_comments_post_id_posts')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_comments'))
    )
    op.create_table('likes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], name=op.f('fk_likes_post_id_posts')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_likes'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('likes')
    op.drop_table('comments')
    op.drop_table('posts')
    # ### end Alembic commands ###
