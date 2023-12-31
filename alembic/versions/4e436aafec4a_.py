"""empty message

Revision ID: 4e436aafec4a
Revises: abd94afc7539
Create Date: 2023-06-26 22:36:16.038350

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e436aafec4a'
down_revision = 'abd94afc7539'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('refresh_token', sa.Column('uuid', sa.UUID(), nullable=False))
    op.add_column('refresh_token', sa.Column('is_active', sa.Boolean(), nullable=True))
    op.add_column('refresh_token', sa.Column('is_created', sa.DateTime(), nullable=False))
    op.add_column('refresh_token', sa.Column('is_updated', sa.DateTime(), nullable=True))
    op.drop_index('ix_refresh_token_id', table_name='refresh_token')
    op.create_index(op.f('ix_refresh_token_uuid'), 'refresh_token', ['uuid'], unique=False)
    op.drop_column('refresh_token', 'id')
    op.add_column('user', sa.Column('is_activate', sa.Boolean(), nullable=False))
    op.add_column('user', sa.Column('created_at', sa.DateTime(timezone=True), nullable=False))
    op.add_column('user', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'updated_at')
    op.drop_column('user', 'created_at')
    op.drop_column('user', 'is_activate')
    op.add_column('refresh_token', sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_index(op.f('ix_refresh_token_uuid'), table_name='refresh_token')
    op.create_index('ix_refresh_token_id', 'refresh_token', ['id'], unique=False)
    op.drop_column('refresh_token', 'is_updated')
    op.drop_column('refresh_token', 'is_created')
    op.drop_column('refresh_token', 'is_active')
    op.drop_column('refresh_token', 'uuid')
    # ### end Alembic commands ###
