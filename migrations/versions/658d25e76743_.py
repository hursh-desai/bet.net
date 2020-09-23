"""empty message

Revision ID: 658d25e76743
Revises: 90f0a554bc32
Create Date: 2020-09-20 15:17:26.113532

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '658d25e76743'
down_revision = '90f0a554bc32'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'events', ['name'])
    op.create_foreign_key(None, 'bets', 'events', ['event_name'], ['name'])
    op.drop_column('bets', 'access')
    op.add_column('events', sa.Column('creator_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'events', 'users', ['creator_id'], ['id'])
    op.drop_column('events', 'decider_url')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('decider_url', sa.VARCHAR(length=30), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'events', type_='foreignkey')
    op.drop_constraint(None, 'events', type_='unique')
    op.drop_column('events', 'creator_id')
    op.add_column('bets', sa.Column('access', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'bets', type_='foreignkey')
    # ### end Alembic commands ###
