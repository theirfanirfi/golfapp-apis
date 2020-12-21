"""notification table added

Revision ID: 003fc5a0dff6
Revises: de6ee4f838e0
Create Date: 2020-12-20 21:57:01.026756

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003fc5a0dff6'
down_revision = 'de6ee4f838e0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notifications',
    sa.Column('notification_id', sa.Integer(), nullable=False),
    sa.Column('is_swap', sa.Integer(), nullable=True),
    sa.Column('is_like', sa.Integer(), nullable=True),
    sa.Column('is_review', sa.Integer(), nullable=True),
    sa.Column('is_share', sa.Integer(), nullable=True),
    sa.Column('status_id', sa.Integer(), nullable=True),
    sa.Column('notifier_user_id', sa.Integer(), nullable=True),
    sa.Column('to_be_notified_user_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.String(length=50), nullable=True),
    sa.Column('updated_at', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('notification_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('notifications')
    # ### end Alembic commands ###
