"""adding spotify user id

Revision ID: f60ae6e944c3
Revises: 
Create Date: 2024-01-14 11:13:41.033252

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f60ae6e944c3'
down_revision = None
branch_labels = None
depends_on = None

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None, naming_convention=naming_convention) as batch_op:
        batch_op.add_column(sa.Column('spotify_user_id', sa.String(length=30), nullable=True))
        batch_op.create_unique_constraint('constraint_spotify_user_id', ['spotify_user_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('spotify_user_id')

    # ### end Alembic commands ###
