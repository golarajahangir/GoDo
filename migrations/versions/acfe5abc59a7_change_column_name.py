"""Change column name

Revision ID: acfe5abc59a7
Revises: 7f591bceb464
Create Date: 2023-02-11 17:54:01.868260

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'acfe5abc59a7'
down_revision = '7f591bceb464'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_done', sa.Boolean(), nullable=True))
        batch_op.drop_column('status')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.BOOLEAN(), nullable=True))
        batch_op.drop_column('is_done')

    # ### end Alembic commands ###
