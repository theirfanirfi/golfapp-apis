"""messages model changed

Revision ID: 78012194f17f
Revises: 752f5695ebe1
Create Date: 2021-01-21 12:44:37.187644

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78012194f17f'
down_revision = '752f5695ebe1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('p_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('message', 'p_id')
    # ### end Alembic commands ###
