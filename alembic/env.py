
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
# IocManager.Base = declarative_base(metadata=MetaData(schema=database_config.schema))
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
from models.dao.integration.PythonDataIntegration import PythonDataIntegration
from models.dao.integration.PythonDataIntegrationConnection import PythonDataIntegrationConnection
from models.dao.integration.PythonDataIntegrationColumn import PythonDataIntegrationColumn
from models.dao.integration.PythonDataIntegrationLog import PythonDataIntegrationLog
from models.dao.integration.PythonDataIntegrationJob import PythonDataIntegrationJob
from models.dao.operation.DataOperation import DataOperation
from models.dao.operation.DataOperationExecution import DataOperationExecution
from models.dao.operation.DataOperationExecutionProcess import DataOperationExecutionProcess
from models.dao.operation.DataOperationExecutionProcessStatus import DataOperationExecutionProcessStatus
from models.dao.operation.DataOperationExecutionStatus import DataOperationExecutionStatus
from models.dao.operation.DataOperationIntegration import DataOperationIntegration


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
    print(f"schema:{database_config.schema}")
    print(f"connection string:{connection_string}")
    
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
    print(f"schema:{database_config.schema}")
    print(f"connection string:{connection_string}")
    connectible = create_engine(connection_string, poolclass=pool.NullPool)
    SCHEMA_NAME = "NOT_test_fktdb"

    def include_object(object, name, type_, reflected, compare_to):
        # print(object.schema)
        if False:#(type_ == "table"):
            return object.schema == 'Common'
        else:
            return True
    if connectible is not None:
        # Create schema; if it already exists, skip this
        try:
            connectible.execute(CreateSchema(database_config.schema))
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
