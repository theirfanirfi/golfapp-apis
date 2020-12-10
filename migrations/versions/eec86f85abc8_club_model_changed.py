"""club model changed

Revision ID: eec86f85abc8
Revises: 793fe44c3506
Create Date: 2020-12-08 19:57:47.372522

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'eec86f85abc8'
down_revision = '793fe44c3506'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('club_description',
    sa.Column('des_id', sa.Integer(), nullable=False),
    sa.Column('des_text', sa.Text(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('club_id', sa.Integer(), nullable=True),
    sa.Column('des_media', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('des_id')
    )
    op.drop_column('clubs', 'club_media')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('clubs', sa.Column('club_media', mysql.TEXT(), nullable=True))
    op.drop_table('club_description')
    # ### end Alembic commands ###
