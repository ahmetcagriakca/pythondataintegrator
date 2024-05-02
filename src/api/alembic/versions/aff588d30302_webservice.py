"""webservice

Revision ID: aff588d30302
Revises: 5ba56f7f0943
Create Date: 2022-03-13 16:52:25.859248

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'aff588d30302'
down_revision = '5ba56f7f0943'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ConnectionWebService',
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('ConnectionId', sa.Integer(), nullable=True),
    sa.Column('ConnectorTypeId', sa.Integer(), nullable=True),
    sa.Column('Ssl', sa.Boolean(), nullable=True),
    sa.Column('CreatedByUserId', sa.Integer(), nullable=False),
    sa.Column('CreationDate', sa.DateTime(), nullable=False),
    sa.Column('LastUpdatedUserId', sa.Integer(), nullable=True),
    sa.Column('LastUpdatedDate', sa.DateTime(), nullable=True),
    sa.Column('IsDeleted', sa.Integer(), nullable=False),
    sa.Column('Comments', sa.String(length=1000), nullable=True),
    sa.ForeignKeyConstraint(['ConnectionId'], ['Connection.Connection.Id'], ),
    sa.ForeignKeyConstraint(['ConnectorTypeId'], ['Connection.ConnectorType.Id'], ),
    sa.PrimaryKeyConstraint('Id'),
    schema='Connection'
    )
    op.create_table('ConnectionWebServiceSoap',
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('ConnectionWebServiceId', sa.Integer(), nullable=True),
    sa.Column('Wsdl', sa.String(length=500), nullable=True),
    sa.Column('CreatedByUserId', sa.Integer(), nullable=False),
    sa.Column('CreationDate', sa.DateTime(), nullable=False),
    sa.Column('LastUpdatedUserId', sa.Integer(), nullable=True),
    sa.Column('LastUpdatedDate', sa.DateTime(), nullable=True),
    sa.Column('IsDeleted', sa.Integer(), nullable=False),
    sa.Column('Comments', sa.String(length=1000), nullable=True),
    sa.ForeignKeyConstraint(['ConnectionWebServiceId'], ['Connection.ConnectionWebService.Id'], ),
    sa.PrimaryKeyConstraint('Id'),
    schema='Connection'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ConnectionWebServiceSoap', schema='Connection')
    op.drop_table('ConnectionWebService', schema='Connection')
    # ### end Alembic commands ###