"""swaps table added

Revision ID: 4fb062a055a2
Revises: f6bb0a61a19c
Create Date: 2020-11-21 17:18:23.258451

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4fb062a055a2'
down_revision = 'f6bb0a61a19c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('swaps',
    sa.Column('swap_id', sa.Integer(), nullable=False),
    sa.Column('is_status', sa.Integer(), nullable=True),
    sa.Column('is_player', sa.Integer(), nullable=True),
    sa.Column('is_club', sa.Integer(), nullable=True),
    sa.Column('swaper_id', sa.Integer(), nullable=True),
    sa.Column('swaped_with_id', sa.Integer(), nullable=True),
    sa.Column('status_id', sa.Integer(), nullable=True),
    sa.Column('player_id', sa.Integer(), nullable=True),
    sa.Column('club_id', sa.Integer(), nullable=True),
    sa.Column('is_accepted', sa.Integer(), nullable=True),
    sa.Column('is_rejected', sa.Integer(), nullable=True),
    sa.Column('is_expired', sa.Integer(), nullable=True),
    sa.Column('is_reviewed', sa.Integer(), nullable=True),
    sa.Column('review_rating', sa.Integer(), nullable=True),
    sa.Column('review_desc', sa.Text(), nullable=True),
    sa.Column('created_at', sa.String(length=50), nullable=True),
    sa.Column('updated_at', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('swap_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('swaps')
    # ### end Alembic commands ###
