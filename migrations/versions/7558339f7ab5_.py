"""empty message

Revision ID: 7558339f7ab5
Revises: 1f48e1c77cf5
Create Date: 2017-07-01 12:55:25.938255

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7558339f7ab5'
down_revision = '1f48e1c77cf5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reminder',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('text', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reminder')
    # ### end Alembic commands ###
