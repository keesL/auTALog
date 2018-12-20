"""empty message

Revision ID: 8ba179f2ac14
Revises: 00c6daf0d96c
Create Date: 2018-12-19 21:45:28.045426

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ba179f2ac14'
down_revision = '00c6daf0d96c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tutoring_session', sa.Column('summary', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tutoring_session', 'summary')
    # ### end Alembic commands ###
