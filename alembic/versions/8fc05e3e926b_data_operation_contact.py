"""data_operation_contact

Revision ID: 8fc05e3e926b
Revises: c207709fadb3
Create Date: 2021-01-11 01:28:56.174549

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8fc05e3e926b'
down_revision = 'c207709fadb3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('DataOperationContact',
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('DataOperationId', sa.Integer(), nullable=True),
    sa.Column('Email', sa.String(length=250), nullable=False),
    sa.Column('CreatedByUserId', sa.Integer(), nullable=False),
    sa.Column('CreationDate', sa.DateTime(), nullable=False),
    sa.Column('LastUpdatedUserId', sa.Integer(), nullable=True),
    sa.Column('LastUpdatedDate', sa.DateTime(), nullable=True),
    sa.Column('IsDeleted', sa.Integer(), nullable=False),
    sa.Column('Comments', sa.String(length=1000), nullable=True),
    sa.Column('RowVersion', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['DataOperationId'], ['Operation.DataOperation.Id'], ),
    sa.PrimaryKeyConstraint('Id'),
    schema='Operation'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('DataOperationContact', schema='Operation')
    # ### end Alembic commands ###