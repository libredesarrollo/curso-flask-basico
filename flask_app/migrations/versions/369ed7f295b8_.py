"""empty message

Revision ID: 369ed7f295b8
Revises: d0c81368745c
Create Date: 2020-03-07 06:27:59.222138

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '369ed7f295b8'
down_revision = 'd0c81368745c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_active', sa.Boolean(), server_default='1', nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_active')
    # ### end Alembic commands ###
