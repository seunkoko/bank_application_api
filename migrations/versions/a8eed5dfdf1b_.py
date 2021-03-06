"""empty message

Revision ID: a8eed5dfdf1b
Revises: 92708379942d
Create Date: 2018-05-25 15:36:35.614194

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8eed5dfdf1b'
down_revision = '92708379942d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Transaction', sa.Column('transaction_amount', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Transaction', 'transaction_amount')
    # ### end Alembic commands ###
