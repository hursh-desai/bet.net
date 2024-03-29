"""empty message

Revision ID: c76486ba722f
Revises: e20d8c96f7de
Create Date: 2020-11-17 23:31:46.831175

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c76486ba722f'
down_revision = 'e20d8c96f7de'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('agreements', sa.Column('date', sa.DateTime(timezone=True), nullable=True))
    op.create_index(op.f('ix_agreements_date'), 'agreements', ['date'], unique=False)
    op.alter_column('bets', 'bet_amount', new_column_name='amount')
    op.add_column('users', sa.Column('date', sa.DateTime(timezone=True), nullable=True))
    op.create_index(op.f('ix_users_date'), 'users', ['date'], unique=False)
    op.create_index('name_tsv', 'events',
            [sa.text("to_tsvector('english', name)")],
            postgresql_using='gin')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_date'), table_name='users')
    op.drop_column('users', 'date')
    op.alter_column('bets', 'amount', new_column_name='bet_amount')
    op.drop_index(op.f('ix_agreements_date'), table_name='agreements')
    op.drop_column('agreements', 'date')
    op.drop_index('name_tsv')
    # ### end Alembic commands ###
