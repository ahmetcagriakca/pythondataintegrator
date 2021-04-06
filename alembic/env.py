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
api_config: ApiConfig = config_manager.get(ApiConfig)
database_config: DatabaseConfig = config_manager.get(DatabaseConfig)
connection_string = Utils.get_connection_string(database_config=database_config)

from infrastructor.IocManager import IocManager

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
# dao_folder = os.path.join(root_directory, 'models', 'dao')
# folders = Utils.find_sub_folders(dao_folder)
# module_list, module_attr_list = Utils.get_modules(folders)

# aps
from models.dao.aps import ApSchedulerJob, ApSchedulerEvent, ApSchedulerJobEvent, ApSchedulerJobsTable

# connection
from models.dao.connection import Connection, ConnectionDatabase, ConnectorType, ConnectionType, ConnectionFile, \
    ConnectionSecret, ConnectionQueue, ConnectionServer


# integration
from models.dao.integration import DataIntegration, DataIntegrationConnection, \
    DataIntegrationColumn, DataIntegrationConnectionDatabase, DataIntegrationConnectionFile, \
    DataIntegrationConnectionFileCsv,DataIntegrationConnectionQueue

# common
from models.dao.common import Log, OperationEvent, Status, ConfigParameter, OperationEvent

# operation
from models.dao.operation import DataOperation, DataOperationIntegration, DataOperationJobExecution, \
    DataOperationJobExecutionEvent, DataOperationJobExecutionIntegration, DataOperationJobExecutionIntegrationEvent, \
    DataOperationJob, DataOperationContact, Definition

# secret
from models.dao.secret import Secret, SecretType, SecretSourceBasicAuthentication, SecretSource, AuthenticationType

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
        if False:  # (type_ == "table"):
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
