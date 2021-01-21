"""message model changed

Revision ID: 42e6979d4c7a
Revises: 78012194f17f
Create Date: 2021-01-21 12:56:59.323093

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '42e6979d4c7a'
down_revision = '78012194f17f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('is_read', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('message', 'is_read')
    # ### end Alembic commands ###