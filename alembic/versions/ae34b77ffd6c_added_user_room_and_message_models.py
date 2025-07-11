"""Added user, room, and message models

Revision ID: ae34b77ffd6c
Revises: 5c5cd270e2f4
Create Date: 2025-07-08 09:18:56.494509

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ae34b77ffd6c'
down_revision: Union[str, Sequence[str], None] = '5c5cd270e2f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('messages', 'content',
               existing_type=sa.VARCHAR(),
               type_=sa.Text(),
               nullable=True)
    op.alter_column('messages', 'timestamp',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               type_=sa.DateTime(),
               existing_nullable=True,
               existing_server_default=sa.text('now()'))
    op.alter_column('rooms', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_constraint(op.f('rooms_name_key'), 'rooms', type_='unique')
    op.create_index(op.f('ix_rooms_name'), 'rooms', ['name'], unique=True)
    op.drop_column('rooms', 'description')
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('users', 'hashed_password',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('users', 'role',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_constraint(op.f('users_username_key'), 'users', type_='unique')
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.create_unique_constraint(op.f('users_username_key'), 'users', ['username'], postgresql_nulls_not_distinct=False)
    op.alter_column('users', 'role',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('users', 'hashed_password',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.add_column('rooms', sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_rooms_name'), table_name='rooms')
    op.create_unique_constraint(op.f('rooms_name_key'), 'rooms', ['name'], postgresql_nulls_not_distinct=False)
    op.alter_column('rooms', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('messages', 'timestamp',
               existing_type=sa.DateTime(),
               type_=postgresql.TIMESTAMP(timezone=True),
               existing_nullable=True,
               existing_server_default=sa.text('now()'))
    op.alter_column('messages', 'content',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
