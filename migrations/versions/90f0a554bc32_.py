"""empty message

Revision ID: 90f0a554bc32
Revises: 31592ff17e66
Create Date: 2020-09-18 18:36:16.586521

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90f0a554bc32'
down_revision = '31592ff17e66'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('moderator_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'events', 'users', ['moderator_id'], ['id'])
    op.create_index('event_name_tsv', 'bets',
            [sa.text("to_tsvector('english', event_name)")],
            postgresql_using='gin')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'events', type_='foreignkey')
    op.drop_column('events', 'moderator_id')
    op.drop_index('event_name_tsv')
    # ### end Alembic commands ###
