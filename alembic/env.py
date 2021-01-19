
import sys

sys.path = ['', '..'] + sys.path[1:]
print(sys.path[1:])
import os

import sqlalchemy
from sqlalchemy.sql.ddl import CreateSchema

from logging.config import fileConfig

from sqlalchemy import create_engine
from sqlalchemy import pool

from alembic import context

from infrastructor.utils.Utils import Utils
from models.configs.ApiConfig import ApiConfig
from models.configs.DatabaseConfig import DatabaseConfig
from infrastructor.utils.ConfigManager import ConfigManager
root_directory = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

config_manager = ConfigManager(root_directory)
# ApiConfig gettin with type
api_config: ApiConfig = config_manager.get(ApiConfig)
database_config: DatabaseConfig = config_manager.get(DatabaseConfig)
connection_string = Utils.get_connection_string(database_config=database_config)

from infrastructor.IocManager import IocManager
#this is the Alembic Config object, which provides
#access to the values within the .ini file in use.

from models.dao.aps.ApSchedulerJob import ApSchedulerJob
from models.dao.aps.ApSchedulerEvent import ApSchedulerEvent
from models.dao.aps.ApSchedulerJobEvent import ApSchedulerJobEvent
from models.dao.aps.ApSchedulerJobsTable import ApSchedulerJobsTable
from models.dao.connection.ConnectorType import ConnectorType
from models.dao.connection.ConnectionType import ConnectionType
from models.dao.connection.Connection import Connection
from models.dao.connection.ConnectionDatabase import ConnectionDatabase
from models.dao.integration.DataIntegration import DataIntegration
from models.dao.integration.DataIntegrationConnection import DataIntegrationConnection
from models.dao.integration.DataIntegrationColumn import DataIntegrationColumn
from models.dao.common.Log import Log
from models.dao.common.OperationEvent import OperationEvent
from models.dao.common.Status import Status
from models.dao.operation.DataOperation import DataOperation
from models.dao.operation.DataOperationIntegration import DataOperationIntegration
from models.dao.operation.DataOperationJobExecution import DataOperationJobExecution
from models.dao.operation.DataOperationJobExecutionEvent import DataOperationJobExecutionEvent
from models.dao.operation.DataOperationJob import DataOperationJob
from models.dao.operation.DataOperationContact import DataOperationContact
from models.dao.common.ConfigParameter import ConfigParameter

config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = IocManager.Base.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    print(f"run_migrations_offline")
    print(f"environment:{api_config.environment}")
    
    if connection_string is not None and connection_string != "":
        context.configure(
            url=connection_string,
            target_metadata=target_metadata,
            literal_binds=True,
            compare_type=True,
            compare_server_default=True,
            include_schemas=True,
            dialect_opts={"paramstyle": "named"},
            version_table='AlembicVersion',
            version_table_schema='Common'
        )

    with context.begin_transaction():
        context.run_migrations()
    # url = config.get_main_option("sqlalchemy.url")
    # context.configure(
    #     url=url,
    #     target_metadata=target_metadata,
    #     literal_binds=True,
    #     dialect_opts={"paramstyle": "named"},
    #     version_table='AlembicVersion',
    #     version_table_schema='ONENT.NEMS_INTEGRATION'
    # )

    # with context.begin_transaction():
    #     context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectible = None
    print(f"run_migrations_online")
    print(f"environment:{api_config.environment}")
    print(f"connection string:{connection_string}")
    connectible = create_engine(connection_string, poolclass=pool.NullPool)
    SCHEMA_NAME = "NOT_test_fktdb"

    def include_object(object, name, type_, reflected, compare_to):
        if False:#(type_ == "table"):
            return object.schema == 'Common'
        else:
            return True
    if connectible is not None:
        # Create schema; if it already exists, skip this
        try:
            connectible.execute(CreateSchema("Common"))
        except sqlalchemy.exc.ProgrammingError:
            pass
        with connectible.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                compare_type=True,
                compare_server_default=True,
                include_schemas=True,
                version_table='AlembicVersion',
                version_table_schema='Common',
                include_object=include_object
            )

            with context.begin_transaction():
                context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
