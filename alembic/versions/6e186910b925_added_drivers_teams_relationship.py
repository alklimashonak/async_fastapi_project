"""Added drivers_teams relationship

Revision ID: 6e186910b925
Revises: 2109c7145b63
Create Date: 2023-01-05 23:40:01.265190

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e186910b925'
down_revision = '2109c7145b63'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('drivers_teams',
    sa.Column('driver_id', sa.Integer(), nullable=True),
    sa.Column('team_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['driver_id'], ['drivers.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['team_id'], ['teams.id'], ondelete='CASCADE')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('drivers_teams')
    # ### end Alembic commands ###
