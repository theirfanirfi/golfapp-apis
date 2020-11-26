"""status table created

Revision ID: 020ebc8f0b92
Revises: f52b8de59398
Create Date: 2020-11-07 02:11:42.396712

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '020ebc8f0b92'
down_revision = 'f52b8de59398'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('statuses',
    sa.Column('status_id', sa.Integer(), nullable=False),
    sa.Column('status_description', sa.String(length=200), nullable=False),
    sa.Column('status_media', sa.String(length=200), nullable=True),
    sa.Column('status_link', sa.String(length=200), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('status_type', sa.Integer(), nullable=True),
    sa.Column('is_club_status', sa.Integer(), nullable=True),
    sa.Column('average_rating', sa.Float(), nullable=True),
    sa.Column('created_at', sa.String(length=50), nullable=True),
    sa.Column('updated_at', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('status_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('statuses')
    # ### end Alembic commands ###