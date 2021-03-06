"""empty message

Revision ID: 8665163c4321
Revises:
Create Date: 2019-11-28 23:21:25.944566

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8665163c4321'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("polls") as batch_op:
        batch_op.drop_column('status')
    op.add_column('topics', sa.Column('status', sa.Boolean(), default=1))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('topics', schema=None) as batch_op:
        batch_op.drop_column('status')

    # ### end Alembic commands ###
