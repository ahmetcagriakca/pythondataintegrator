"""baseline

Revision ID: fe12dc8feb82
Revises: 
Create Date: 2021-01-19 23:42:00.695822

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
from apscheduler.events import EVENT_SCHEDULER_STARTED, EVENT_SCHEDULER_SHUTDOWN, EVENT_SCHEDULER_PAUSED

revision = 'fe12dc8feb82'
down_revision = None
branch_labels = None
depends_on = None


def insert_connection_types():
    from models.dao.connection.ConnectionType import ConnectionType
    from models.dao.connection.ConnectorType import ConnectorType
    bind = op.get_bind()
    from sqlalchemy import orm
    session = orm.Session(bind=bind)
    connection_type_list = [
        {
            "Name": "Database",
        },
        {
            "Name": "File",
        },
    ]
    connector_type_list = [
        {
            "ConnectionType": "Database",
            "Name": "MSSQL",
        },
        {
            "ConnectionType": "Database",
            "Name": "ORACLE",
        },
        {
            "ConnectionType": "Database",
            "Name": "POSTGRESQL",
        },
        {
            "ConnectionType": "File",
            "Name": "EXCEL",
        },
        {
            "ConnectionType": "File",
            "Name": "CSV",
        }
    ]
    connection_types = []
    for connection_type_json in connection_type_list:
        connection_type = ConnectionType(Name=connection_type_json["Name"])
        connection_types.append(connection_type)
    session.bulk_save_objects(connection_types)
    session.commit()
    connector_types = []
    for connector_type_json in connector_type_list:
        connection_type = session.query(ConnectionType).filter_by(Name=connector_type_json["ConnectionType"]).first()
        connector_type = ConnectorType(Name=connector_type_json["Name"], ConnectionTypeId=connection_type.Id)
        connector_types.append(connector_type)
    session.bulk_save_objects(connector_types)
    session.commit()


def insert_event_datas():
    from models.dao.aps.ApSchedulerEvent import ApSchedulerEvent
    from apscheduler.events import EVENT_SCHEDULER_STARTED, EVENT_SCHEDULER_SHUTDOWN, EVENT_SCHEDULER_PAUSED, \
        EVENT_SCHEDULER_RESUMED, EVENT_EXECUTOR_ADDED, EVENT_EXECUTOR_REMOVED, EVENT_JOBSTORE_ADDED, \
        EVENT_JOBSTORE_REMOVED, EVENT_ALL_JOBS_REMOVED, EVENT_JOB_ADDED, EVENT_JOB_REMOVED, EVENT_JOB_MODIFIED, \
        EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, EVENT_JOB_MISSED, EVENT_JOB_SUBMITTED, EVENT_JOB_MAX_INSTANCES
    bind = op.get_bind()
    from sqlalchemy import orm
    bind = op.get_bind()
    session = orm.Session(bind=bind)
    events_list = [
        {
            "Code": EVENT_SCHEDULER_STARTED,
            "Name": "EVENT_SCHEDULER_STARTED",
            "Description": "The scheduler was started",
            "Class": "SchedulerEvent"
        },
        {
            "Code": EVENT_SCHEDULER_SHUTDOWN,
            "Name": "EVENT_SCHEDULER_SHUTDOWN",
            "Description": "The scheduler was shut down",
            "Class": "SchedulerEvent"
        },
        {
            "Code": EVENT_SCHEDULER_PAUSED,
            "Name": "EVENT_SCHEDULER_PAUSED",
            "Description": "Job processing in the scheduler was paused",
            "Class": "SchedulerEvent"
        },
        {
            "Code": EVENT_SCHEDULER_RESUMED,
            "Name": "EVENT_SCHEDULER_RESUMED",
            "Description": "Job processing in the scheduler was resumed",
            "Class": "SchedulerEvent"
        },
        {
            "Code": EVENT_EXECUTOR_ADDED,
            "Name": "EVENT_EXECUTOR_ADDED",
            "Description": "An executor was added to the scheduler",
            "Class": "SchedulerEvent"
        },
        {
            "Code": EVENT_EXECUTOR_REMOVED,
            "Name": "EVENT_EXECUTOR_REMOVED",
            "Description": "An executor was removed to the scheduler",
            "Class": "SchedulerEvent"
        },
        {
            "Code": EVENT_JOBSTORE_ADDED,
            "Name": "EVENT_JOBSTORE_ADDED",
            "Description": "A job store was added to the scheduler",
            "Class": "SchedulerEvent"
        },
        {
            "Code": EVENT_JOBSTORE_REMOVED,
            "Name": "EVENT_JOBSTORE_REMOVED",
            "Description": "A job store was removed from the scheduler",
            "Class": "SchedulerEvent"
        },
        {
            "Code": EVENT_ALL_JOBS_REMOVED,
            "Name": "EVENT_ALL_JOBS_REMOVED",
            "Description": "All jobs were removed from either all job stores or one particular job store",
            "Class": "SchedulerEvent"
        },
        {
            "Code": EVENT_JOB_ADDED,
            "Name": "EVENT_JOB_ADDED",
            "Description": "A job was added to a job store",
            "Class": "JobEvent"
        },
        {
            "Code": EVENT_JOB_REMOVED,
            "Name": "EVENT_JOB_REMOVED",
            "Description": "A job was removed from a job store",
            "Class": "JobEvent"
        },
        {
            "Code": EVENT_JOB_MODIFIED,
            "Name": "EVENT_JOB_MODIFIED",
            "Description": "A job was modified from outside the scheduler",
            "Class": "JobEvent"
        },
        {
            "Code": EVENT_JOB_SUBMITTED,
            "Name": "EVENT_JOB_SUBMITTED",
            "Description": "A job was submitted to its executor to be run",
            "Class": "JobSubmissionEvent"
        },
        {
            "Code": EVENT_JOB_MAX_INSTANCES,
            "Name": "EVENT_JOB_MAX_INSTANCES",
            "Description": "A job being submitted to its executor was not accepted by the executor because the job has already reached its maximum concurrently executing instances",
            "Class": "JobSubmissionEvent"
        },
        {
            "Code": EVENT_JOB_EXECUTED,
            "Name": "EVENT_JOB_EXECUTED",
            "Description": "A job was executed successfully",
            "Class": "JobExecutionEvent"
        },
        {
            "Code": EVENT_JOB_ERROR,
            "Name": "EVENT_JOB_ERROR",
            "Description": "A job raised an exception during execution",
            "Class": "JobExecutionEvent"
        },
        {
            "Code": EVENT_JOB_MISSED,
            "Name": "EVENT_JOB_MISSED",
            "Description": "A job’s execution was missed",
            "Class": "JobExecutionEvent"
        }
    ]
    events = []
    for eventJson in events_list:
        event = ApSchedulerEvent(Code=eventJson["Code"], Name=eventJson["Name"], Description=eventJson["Description"],
                                 Class=eventJson["Class"])

        events.append(event)
    session.bulk_save_objects(events)
    session.commit()


def insert_statuses():
    from models.dao.common.Status import Status
    bind = op.get_bind()
    from sqlalchemy import orm
    session = orm.Session(bind=bind)
    status_list = [
        {
            "Id": 1,
            "Name": "Initialized",
            "Description": "Initialized",
        },
        {
            "Id": 2,
            "Name": "Start",
            "Description": "Start",
        },
        {
            "Id": 3,
            "Name": "Finish",
            "Description": "Finish",
        },
        {
            "Id": 4,
            "Name": "Error",
            "Description": "Error",
        },
    ]
    statuses = []
    for status_json in status_list:
        status = Status(
            Name=status_json["Name"],
            Description=status_json["Description"]
        )
        statuses.append(status)
    session.bulk_save_objects(statuses)
    session.commit()


def insert_event_datas():
    from models.enums.events import EVENT_EXECUTION_INITIALIZED, EVENT_EXECUTION_FINISHED, EVENT_EXECUTION_STARTED, \
        EVENT_EXECUTION_INTEGRATION_STARTED, EVENT_EXECUTION_INTEGRATION_EXECUTE_PRE_PROCEDURE, \
        EVENT_EXECUTION_INTEGRATION_EXECUTE_POST_PROCEDURE, EVENT_EXECUTION_INTEGRATION_EXECUTE_TRUNCATE, \
        EVENT_EXECUTION_INTEGRATION_EXECUTE_QUERY, EVENT_EXECUTION_INTEGRATION_EXECUTE_OPERATION
    from models.dao.common.OperationEvent import OperationEvent
    bind = op.get_bind()
    from sqlalchemy import orm
    session = orm.Session(bind=bind)
    events_list = [
        {
            "Code": EVENT_EXECUTION_INITIALIZED,
            "Name": "EVENT_EXECUTION_INITIALIZED",
            "Description": "Execution initialized",
            "Class": "DataOperationJobExecution"
        },
        {
            "Code": EVENT_EXECUTION_STARTED,
            "Name": "EVENT_EXECUTION_STARTED",
            "Description": "Execution started",
            "Class": "DataOperationJobExecution"
        },
        {
            "Code": EVENT_EXECUTION_FINISHED,
            "Name": "EVENT_EXECUTION_FINISHED",
            "Description": "Execution finished",
            "Class": "DataOperationJobExecution"
        },
        {
            "Code": EVENT_EXECUTION_INTEGRATION_STARTED,
            "Name": "EVENT_EXECUTION_INTEGRATION_STARTED",
            "Description": "Execution integration started",
            "Class": "DataOperationJobExecutionIntegration"
        },
        {
            "Code": EVENT_EXECUTION_INTEGRATION_EXECUTE_PRE_PROCEDURE,
            "Name": "EVENT_EXECUTION_INTEGRATION_EXECUTE_PRE_PROCEDURE",
            "Description": "Execution integration pre procedure executed",
            "Class": "DataOperationJobExecutionIntegration"
        },
        {
            "Code": EVENT_EXECUTION_INTEGRATION_EXECUTE_POST_PROCEDURE,
            "Name": "EVENT_EXECUTION_INTEGRATION_EXECUTE_POST_PROCEDURE",
            "Description": "Execution integration post procedure executed",
            "Class": "DataOperationJobExecutionIntegration"
        },
        {
            "Code": EVENT_EXECUTION_INTEGRATION_EXECUTE_TRUNCATE,
            "Name": "EVENT_EXECUTION_INTEGRATION_EXECUTE_TRUNCATE",
            "Description": "Execution integration truncate executed",
            "Class": "DataOperationJobExecutionIntegration"
        },
        {
            "Code": EVENT_EXECUTION_INTEGRATION_EXECUTE_QUERY,
            "Name": "EVENT_EXECUTION_INTEGRATION_EXECUTE_QUERY",
            "Description": "Execution integration query executed",
            "Class": "DataOperationJobExecutionIntegration"
        },
        {
            "Code": EVENT_EXECUTION_INTEGRATION_EXECUTE_OPERATION,
            "Name": "EVENT_EXECUTION_INTEGRATION_EXECUTE_OPERATION",
            "Description": "Execution integration operation executed",
            "Class": "DataOperationJobExecutionIntegration"
        }
    ]
    events = []
    for eventJson in events_list:
        event = OperationEvent(Code=eventJson["Code"], Name=eventJson["Name"], Description=eventJson["Description"],
                               Class=eventJson["Class"])

        events.append(event)
    session.bulk_save_objects(events)
    session.commit()


def upgrade():
    op.execute('CREATE SCHEMA "Aps"')
    op.execute('CREATE SCHEMA "Connection"')
    op.execute('CREATE SCHEMA "Integration"')
    op.execute('CREATE SCHEMA "Operation"')
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ApSchedulerEvent',
                    sa.Column('Id', sa.Integer(), nullable=False),
                    sa.Column('Code', sa.Integer(), nullable=False),
                    sa.Column('Name', sa.String(length=255), nullable=False),
                    sa.Column('Description', sa.String(length=1000), nullable=False),
                    sa.Column('Class', sa.String(length=255), nullable=False),
                    sa.Column('CreatedByUserId', sa.Integer(), nullable=False),
                    sa.Column('CreationDate', sa.DateTime(), nullable=False),
                    sa.Column('LastUpdatedUserId', sa.Integer(), nullable=True),
                    sa.Column('LastUpdatedDate', sa.DateTime(), nullable=True),
                    sa.Column('IsDeleted', sa.Integer(), nullable=False),
                    sa.Column('Comments', sa.String(length=1000), nullable=True),
                    sa.Column('RowVersion', sa.TIMESTAMP(), nullable=True),
                    sa.PrimaryKeyConstraint('Id'),
                    schema='Aps'
                    )
    op.create_table('ApSchedulerJob',
                    sa.Column('Id', sa.Integer(), nullable=False),
                    sa.Column('JobId', sa.Unicode(length=191), nullable=True),
                    sa.Column('NextRunTime', sa.DateTime(), nullable=True),
                    sa.Column('FuncRef', sa.String(length=500), nullable=False),
                    sa.Column('CreatedByUserId', sa.Integer(), nullable=False),
                    sa.Column('CreationDate', sa.DateTime(), nullable=False),
                    sa.Column('LastUpdatedUserId', sa.Integer(), nullable=True),
                    sa.Column('LastUpdatedDate', sa.DateTime(), nullable=True),
                    sa.Column('IsDeleted', sa.Integer(), nullable=False),
                    sa.Column('Comments', sa.String(length=1000), nullable=True),
                    sa.Column('RowVersion', sa.TIMESTAMP(), nullable=True),
                    sa.PrimaryKeyConstraint('Id'),
                    schema='Aps'
                    )
    op.create_table('ApSchedulerJobsTable',
                    sa.Column('id', sa.Unicode(length=191), nullable=False),
                    sa.Column('next_run_time', sa.Float(precision=25), nullable=True),
                    sa.Column('job_state', sa.LargeBinary(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    schema='Aps'
                    )
    op.create_index(op.f('ix_Aps_ApSchedulerJobsTable_next_run_time'), 'ApSchedulerJobsTable', ['next_run_time'],
                    unique=False, schema='Aps')
    op.create_table('ConfigParameter',
                    sa.Column('Id', sa.Integer(), nullable=False),
                    sa.Column('Name', sa.String(length=255), nullable=False),
                    sa.Column('Type', sa.String(length=255), nullable=True),
                    sa.Column('Value', sa.String(length=255), nullable=False),
                    sa.Column('Description', sa.String(length=1000), nullable=False),
                    sa.Column('CreatedByUserId', sa.Integer(), nullable=False),
                    sa.Column('CreationDate', sa.DateTime(), nullable=False),
                    sa.Column('LastUpdatedUserId', sa.Integer(), nullable=True),
                    sa.Column('LastUpdatedDate', sa.DateTime(), nullable=True),
                    sa.Column('IsDeleted', sa.Integer(), nullable=False),
                    sa.Column('Comments', sa.String(length=1000), nullable=True),
                    sa.Column('RowVersion', sa.TIMESTAMP(), nullable=True),
                    sa.PrimaryKeyConstraint('Id'),
                    schema='Common'
                    )
    op.create_table('Log',
                    sa.Column('Id', sa.Integer(), nullable=False),
                    sa.Column('TypeId', sa.Integer(), nullable=False),
                    sa.Column('Content', sa.String(length=4000), nullable=True),
                    sa.Column('LogDatetime', sa.DateTime(), nullable=True),
                    sa.Column('JobId', sa.Integer(), nullable=True),
                    sa.Column('CreatedByUserId', sa.Integer(), nullable=False),
                    sa.Column('CreationDate', sa.DateTime(), nullable=False),
                    sa.Column('LastUpdatedUserId', sa.Integer(), nullable=True),
                    sa.Column('LastUpdatedDate', sa.DateTime(), nullable=True),
                    sa.Column('IsDeleted', sa.Integer(), nullable=False),
                    sa.Column('Comments', sa.String(length=1000), nullable=True),
                    sa.Column('RowVersion', sa.TIMESTAMP(), nullable=True),
                    sa.PrimaryKeyConstraint('Id'),
                    schema='Common'
                    )
    op.create_index(op.f('ix_Common_Log_JobId'), 'Log', ['JobId'], unique=False, schema='Common')
    op.create_index(op.f('ix_Common_Log_TypeId'), 'Log', ['TypeId'], unique=False, schema='Common')
    op.create_table('OperationEvent',
                    sa.Column('Id', sa.Integer(), nullable=False),
                    sa.Column('Code', sa.Integer(), nullable=False),
                    sa.Column('Name', sa.String(length=100), nullable=False),
                    sa.Column('Description', sa.String(length=250), nullable=False),
                    sa.Column('Class', sa.String(length=255), nullable=False),
                    sa.Column('CreatedByUserId', sa.Integer(), nullable=False),
                    sa.Column('CreationDate', sa.DateTime(), nullable=False),
                    sa.Column('LastUpdatedUserId', sa.Integer(), nullable=True),
                    sa.Column('LastUpdatedDate', sa.DateTime(), nullable=True),
                    sa.Column('IsDeleted', sa.Integer(), nullable=False),
                    sa.Column('Comments', sa.String(length=1000), nullable=True),
                    sa.Column('RowVersion', sa.TIMESTAMP(), nullable=True),
                    sa.PrimaryKeyConstraint('Id'),
                    sa.UniqueConstraint('Code'),
                    schema='Common'
                    )
    op.create_table('Status',
                    sa.Column('Id', sa.Integer(), nullable=False),
                    sa.Column('Name', sa.String(length=100), nullable=False),
                    sa.Column('Description', sa.String(length=250), nullable=False),
                    sa.Column('CreatedByUserId', sa.Integer(), nullable=False),
                    sa.Column('CreationDate', sa.DateTime(), nullable=False),
                    sa.Column('LastUpdatedUserId', sa.Integer(), nullable=True),
                    sa.Column('LastUpdatedDate', sa.DateTime(), nullable=True),
                    sa.Column('IsDeleted', sa.Integer(), nullable=False),
                    sa.Column('Comments', sa.String(length=1000), nullable=True),
                    sa.Column('RowVersion', sa.TIMESTAMP(), nullable=True),
                    sa.PrimaryKeyConstraint('Id'),
                    schema='Common'
                    )
    op.create_table('ConnectionType',
                    sa.Column('Id', sa.Integer(), nullable=False),
                    sa.Column('Name', sa.String(length=100), nullable=False),
                    sa.Column('CreatedByUserId', sa.Integer(), nullable=False),
                    sa.Column('CreationDate', sa.DateTime(), nullable=False),
                    sa.Column('LastUpdatedUserId', sa.Integer(), nullable=True),
                    sa.Column('LastUpdatedDate', sa.DateTime(), nullable=True),
                    sa.Column('IsDeleted', sa.Integer(), nullable=False),
                    sa.Column('Comments', sa.String(length=1000), nullable=True),
                    sa.Column('RowVersion', sa.TIMESTAMP(), nullable=True),
                    sa.PrimaryKeyConstraint('Id'),
                    sa.UniqueConstraint('Name'),
                    schema='Connection'
                    )
    op.create_table('Definition',
                    sa.Column('Id', sa.Integer(), nullable=False),
                    sa.Column('Name', sa.String(length=100), nullable=False),
                    sa.Column('Version', sa.Integer(), nullable=False),
                    sa.Column('Content', sa.Text(), nullable=True),
                    sa.Column('IsActive', sa.Integer(), nullable=False),
                    sa.Column('CreatedByUserId', sa.Integer(), nullable=False),
                    sa.Column('CreationDate', sa.DateTime(), nullable=False),
                    sa.Column('LastUpdatedUserId', sa.Integer(), nullable=True),
                    sa.Column('LastUpdatedDate', sa.DateTime(), nullable=True),
                    sa.Column('IsDeleted', sa.Integer(), nullable=False),
                    sa.Column('Comments', sa.String(length=1000), nullable=True),
                    sa.Column('RowVersion', sa.TIMESTAMP(), nullable=True),
                    sa.PrimaryKeyConstraint('Id'),
                    schema='Operation'
                    )
    op.create_table('ApSchedulerJobEvent',
                    sa.Column('Id', sa.Integer(), nullable=False),
                    sa.Column('ApSchedulerJobId', sa.Integer(), nullable=True),
                    sa.Column('EventId', sa.Integer(), nullable=True),
                    sa.Column('CreatedByUserId', sa.Integer(), nullable=False),
                    sa.Column('CreationDate', sa.DateTime(), nullable=False),
                    sa.Column('LastUpdatedUserId', sa.Integer(), nullable=True),
                    sa.Column('LastUpdatedDate', sa.DateTime(), nullable=True),
                    sa.Column('IsDeleted', sa.Integer(), nullable=False),
                    sa.Column('Comments', sa.String(length=1000), nullable=True),
                    sa.Column('RowVersion', sa.TIMESTAMP(), nullable=True),
                    sa.ForeignKeyConstraint(['ApSchedulerJobId'], ['Aps.ApSchedulerJob.Id'], ),
                    sa.ForeignKeyConstraint(['EventId'], ['Aps.ApSchedulerEvent.Id'], ),
                    sa.PrimaryKeyConstraint('Id'),
                    schema='Aps'
                    )
    op.create_table('Connection',
                    sa.Column('Id', sa.Integer(), nullable=False),
                    sa.Column('Name', sa.String(length=100), nullable=False),
                    sa.Column('ConnectionTypeId', sa.Integer(), nullable=True),
                    sa.Column('CreatedByUserId', sa.Integer(), nullable=False),
                    sa.Column('CreationDate', sa.DateTime(), nullable=False),
                    sa.Column('LastUpdatedUserId', sa.Integer(), nullable=True),
                    sa.Column('LastUpdatedDate', sa.DateTime(), nullable=True),
                    sa.Column('IsDeleted', sa.Integer(), nullable=False),
                    sa.Column('Comments', sa.String(length=1000), nullable=True),
                    sa.Column('RowVersion', sa.TIMESTAMP(), nullable=True),
                    sa.ForeignKeyConstraint(['ConnectionTypeId'], ['Connection.ConnectionType.Id'], ),
                    sa.PrimaryKeyConstraint('Id'),
                    schema='Connection'
                    )
    op.create_index(op.f('ix_Connection_Connection_Name'), 'Connection', ['Name'], unique=True, schema='Connection')
    op.create_table('ConnectorType',
                    sa.Column('Id', sa.Integer(), nullable=False),
                    sa.Column('ConnectionTypeId', sa.Integer(), nullable=True),
                    sa.Column('Name', sa.String(length=100), nullable=False),
                    sa.Column('CreatedByUserId', sa.Integer(), nullable=False),
                    sa.Column('CreationDate', sa.DateTime(), nullable=False),
                    sa.Column('LastUpdatedUserId', sa.Integer(), nullable=True),
                    sa.Column('LastUpdatedDate', sa.DateTime(), nullable=True),
                    sa.Column('IsDeleted', sa.Integer(), nullable=False),
                    sa.Column('Comments', sa.String(length=1000), nullable=True),
                    sa.Column('RowVersion', sa.TIMESTAMP(), nullable=True),
                    sa.ForeignKeyConstraint(['ConnectionTypeId'], ['Connection.ConnectionType.Id'], ),
                    sa.PrimaryKeyConstraint('Id'),
                    sa.UniqueConstraint('Name'),
                    schema='Connection'
                    )
    op.create_table('DataIntegration',
                    sa.Column('Id', sa.Integer(), nullable=False),
                    sa.Column('DefinitionId', sa.Integer(), nullable=True),
                    sa.Column('Code', sa.String(length=100), nullable=False),
                    sa.Column('IsTargetTruncate', sa.Boolean(), nullable=True),
                    sa.Column('IsDelta', sa.Boolean(), nullable=True),
                    sa.Column('CreatedByUserId', sa.Integer(), nullable=False),
                    sa.Column('CreationDate', sa.DateTime(), nullable=False),
                    sa.Column('LastUpdatedUserId', sa.Integer(), nullable=True),
                    sa.Column('LastUpdatedDate', sa.DateTime(), nullable=True),
                    sa.Column('IsDeleted', sa.Integer(), nullable=False),
                    sa.Column('Comments', sa.String(length=1000), nullable=True),
                    sa.Column('RowVersion', sa.TIMESTAMP(), nullable=True),
                    sa.ForeignKeyConstraint(['DefinitionId'], ['Operation.Definition.Id'], ),
                    sa.PrimaryKeyConstraint('Id'),
                    schema='Integration'
                    )
    op.create_index(op.f('ix_Integration_DataIntegration_Code'), 'DataIntegration', ['Code'], unique=True,
                    schema='Integration')
    op.create_table('DataOperation',
                    sa.Column('Id', sa.Integer(), nullable=False),
                    sa.Column('DefinitionId', sa.Integer(), nullable=True),
                    sa.Column('Name', sa.String(length=100), nullable=False),
                    sa.Column('CreatedByUserId', sa.Integer(), nullable=False),
                    sa.Column('CreationDate', sa.DateTime(), nullable=False),
                    sa.Column('LastUpdatedUserId', sa.Integer(), nullable=True),
                    sa.Column('LastUpdatedDate', sa.DateTime(), nullable=True),
                    sa.Column('IsDeleted', sa.Integer(), nullable=False),
                    sa.Column('Comments', sa.String(length=1000), nullable=True),
                    sa.Column('RowVersion', sa.TIMESTAMP(), nullable=True),
                    sa.ForeignKeyConstraint(['DefinitionId'], ['Operation.Definition.Id'], ),
                    sa.PrimaryKeyConstraint('Id'),
                    schema='Operation'
                    )
    op.create_table('ConnectionDatabase',
                    sa.Column('Id', sa.Integer(), nullable=False),
                    sa.Column('ConnectionId', sa.Integer(), nullable=True),
                    sa.Column('ConnectorTypeId', sa.Integer(), nullable=True),
                    sa.Column('Host', sa.String(length=100), nullable=True),
                    sa.Column('Port', sa.Integer(), nullable=True),
                    sa.Column('Sid', sa.String(length=100), nullable=True),
                    sa.Column('ServiceName', sa.String(length=100), nullable=True),
                    sa.Column('DatabaseName', sa.String(length=100), nullable=True),
                    sa.Column('User', sa.String(length=100), nullable=True),
                    sa.Column('Password', sa.String(length=100), nullable=True),
                    sa.Column('CreatedByUserId', sa.Integer(), nullable=False),
                    sa.Column('CreationDate', sa.DateTime(), nullable=False),
                    sa.Column('LastUpdatedUserId', sa.Integer(), nullable=True),
                    sa.Column('LastUpdatedDate', sa.DateTime(), nullable=True),
                    sa.Column('IsDeleted', sa.Integer(), nullable=False),
                    sa.Column('Comments', sa.String(length=1000), nullable=True),
                    sa.Column('RowVersion', sa.TIMESTAMP(), nullable=True),
                    sa.ForeignKeyConstraint(['ConnectionId'], ['Connection.Connection.Id'], ),
                    sa.ForeignKeyConstraint(['ConnectorTypeId'], ['Connection.ConnectorType.Id'], ),
                    sa.PrimaryKeyConstraint('Id'),
                    schema='Connection'
                    )
    op.create_table('DataIntegrationColumn',
                    sa.Column('Id', sa.Integer(), nullable=False),
                    sa.Column('DataIntegrationId', sa.Integer(), nullable=True),
                    sa.Column('ResourceType', sa.String(length=100), nullable=True),
                    sa.Column('SourceColumnName', sa.String(length=100), nullable=True),
                    sa.Column('TargetColumnName', sa.String(length=100), nullable=True),
                    sa.Column('CreatedByUserId', sa.Integer(), nullable=False),
                    sa.Column('CreationDate', sa.DateTime(), nullable=False),
                    sa.Column('LastUpdatedUserId', sa.Integer(), nullable=True),
                    sa.Column('LastUpdatedDate', sa.DateTime(), nullable=True),
                    sa.Column('IsDeleted', sa.Integer(), nullable=False),
                    sa.Column('Comments', sa.String(length=1000), nullable=True),
                    sa.Column('RowVersion', sa.TIMESTAMP(), nullable=True),
                    sa.ForeignKeyConstraint(['DataIntegrationId'], ['Integration.DataIntegration.Id'], ),
                    sa.PrimaryKeyConstraint('Id'),
                    schema='Integration'
                    )
    op.create_table('DataIntegrationConnection',
                    sa.Column('Id', sa.Integer(), nullable=False),
                    sa.Column('DataIntegrationId', sa.Integer(), nullable=True),
                    sa.Column('ConnectionId', sa.Integer(), nullable=True),
                    sa.Column('SourceOrTarget', sa.Integer(), nullable=False),
                    sa.Column('Schema', sa.String(length=100), nullable=True),
                    sa.Column('TableName', sa.String(length=100), nullable=True),
                    sa.Column('Query', sa.Text(), nullable=True),
                    sa.Column('CreatedByUserId', sa.Integer(), nullable=False),
                    sa.Column('CreationDate', sa.DateTime(), nullable=False),
                    sa.Column('LastUpdatedUserId', sa.Integer(), nullable=True),
                    sa.Column('LastUpdatedDate', sa.DateTime(), nullable=True),
                    sa.Column('IsDeleted', sa.Integer(), nullable=False),
                    sa.Column('Comments', sa.String(length=1000), nullable=True),
                    sa.Column('RowVersion', sa.TIMESTAMP(), nullable=True),
                    sa.ForeignKeyConstraint(['ConnectionId'], ['Connection.Connection.Id'], ),
                    sa.ForeignKeyConstraint(['DataIntegrationId'], ['Integration.DataIntegration.Id'], ),
                    sa.PrimaryKeyConstraint('Id'),
                    schema='Integration'
                    )
    op.create_table('DataIntegrationExecutionJob',
                    sa.Column('Id', sa.Integer(), nullable=False),
                    sa.Column('DataIntegrationId', sa.Integer(), nullable=True),
                    sa.Column('ExecutionProcedure', sa.String(length=1000), nullable=True),
                    sa.Column('IsPre', sa.Boolean(), nullable=True),
                    sa.Column('IsPost', sa.Boolean(), nullable=True),
                    sa.Column('CreatedByUserId', sa.Integer(), nullable=False),
                    sa.Column('CreationDate', sa.DateTime(), nullable=False),
                    sa.Column('LastUpdatedUserId', sa.Integer(), nullable=True),
                    sa.Column('LastUpdatedDate', sa.DateTime(), nullable=True),
                    sa.Column('IsDeleted', sa.Integer(), nullable=False),
                    sa.Column('Comments', sa.String(length=1000), nullable=True),
                    sa.Column('RowVersion', sa.TIMESTAMP(), nullable=True),
                    sa.ForeignKeyConstraint(['DataIntegrationId'], ['Integration.DataIntegration.Id'], ),
                    sa.PrimaryKeyConstraint('Id'),
                    schema='Integration'
                    )
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
    op.create_table('DataOperationIntegration',
                    sa.Column('Id', sa.Integer(), nullable=False),
                    sa.Column('DataOperationId', sa.Integer(), nullable=True),
                    sa.Column('DataIntegrationId', sa.Integer(), nullable=True),
                    sa.Column('Order', sa.Integer(), nullable=False),
                    sa.Column('Limit', sa.Integer(), nullable=False),
                    sa.Column('ProcessCount', sa.Integer(), nullable=False),
                    sa.Column('CreatedByUserId', sa.Integer(), nullable=False),
                    sa.Column('CreationDate', sa.DateTime(), nullable=False),
                    sa.Column('LastUpdatedUserId', sa.Integer(), nullable=True),
                    sa.Column('LastUpdatedDate', sa.DateTime(), nullable=True),
                    sa.Column('IsDeleted', sa.Integer(), nullable=False),
                    sa.Column('Comments', sa.String(length=1000), nullable=True),
                    sa.Column('RowVersion', sa.TIMESTAMP(), nullable=True),
                    sa.ForeignKeyConstraint(['DataIntegrationId'], ['Integration.DataIntegration.Id'], ),
                    sa.ForeignKeyConstraint(['DataOperationId'], ['Operation.DataOperation.Id'], ),
                    sa.PrimaryKeyConstraint('Id'),
                    schema='Operation'
                    )
    op.create_table('DataOperationJob',
                    sa.Column('Id', sa.Integer(), nullable=False),
                    sa.Column('DataOperationId', sa.Integer(), nullable=True),
                    sa.Column('ApSchedulerJobId', sa.Integer(), nullable=True),
                    sa.Column('StartDate', sa.DateTime(), nullable=False),
                    sa.Column('EndDate', sa.DateTime(), nullable=True),
                    sa.Column('Cron', sa.String(length=100), nullable=True),
                    sa.Column('CreatedByUserId', sa.Integer(), nullable=False),
                    sa.Column('CreationDate', sa.DateTime(), nullable=False),
                    sa.Column('LastUpdatedUserId', sa.Integer(), nullable=True),
                    sa.Column('LastUpdatedDate', sa.DateTime(), nullable=True),
                    sa.Column('IsDeleted', sa.Integer(), nullable=False),
                    sa.Column('Comments', sa.String(length=1000), nullable=True),
                    sa.Column('RowVersion', sa.TIMESTAMP(), nullable=True),
                    sa.ForeignKeyConstraint(['ApSchedulerJobId'], ['Aps.ApSchedulerJob.Id'], ),
                    sa.ForeignKeyConstraint(['DataOperationId'], ['Operation.DataOperation.Id'], ),
                    sa.PrimaryKeyConstraint('Id'),
                    schema='Operation'
                    )
    op.create_table('DataOperationJobExecution',
                    sa.Column('Id', sa.Integer(), nullable=False),
                    sa.Column('DataOperationJobId', sa.Integer(), nullable=True),
                    sa.Column('DefinitionId', sa.Integer(), nullable=True),
                    sa.Column('StatusId', sa.Integer(), nullable=True),
                    sa.Column('StartDate', sa.DateTime(), nullable=False),
                    sa.Column('EndDate', sa.DateTime(), nullable=True),
                    sa.Column('CreatedByUserId', sa.Integer(), nullable=False),
                    sa.Column('CreationDate', sa.DateTime(), nullable=False),
                    sa.Column('LastUpdatedUserId', sa.Integer(), nullable=True),
                    sa.Column('LastUpdatedDate', sa.DateTime(), nullable=True),
                    sa.Column('IsDeleted', sa.Integer(), nullable=False),
                    sa.Column('Comments', sa.String(length=1000), nullable=True),
                    sa.Column('RowVersion', sa.TIMESTAMP(), nullable=True),
                    sa.ForeignKeyConstraint(['DataOperationJobId'], ['Operation.DataOperationJob.Id'], ),
                    sa.ForeignKeyConstraint(['DefinitionId'], ['Operation.Definition.Id'], ),
                    sa.ForeignKeyConstraint(['StatusId'], ['Common.Status.Id'], ),
                    sa.PrimaryKeyConstraint('Id'),
                    schema='Operation'
                    )
    op.create_table('DataOperationJobExecutionEvent',
                    sa.Column('Id', sa.Integer(), nullable=False),
                    sa.Column('DataOperationJobExecutionId', sa.Integer(), nullable=True),
                    sa.Column('EventId', sa.Integer(), nullable=True),
                    sa.Column('EventDate', sa.DateTime(), nullable=False),
                    sa.Column('CreatedByUserId', sa.Integer(), nullable=False),
                    sa.Column('CreationDate', sa.DateTime(), nullable=False),
                    sa.Column('LastUpdatedUserId', sa.Integer(), nullable=True),
                    sa.Column('LastUpdatedDate', sa.DateTime(), nullable=True),
                    sa.Column('IsDeleted', sa.Integer(), nullable=False),
                    sa.Column('Comments', sa.String(length=1000), nullable=True),
                    sa.Column('RowVersion', sa.TIMESTAMP(), nullable=True),
                    sa.ForeignKeyConstraint(['DataOperationJobExecutionId'],
                                            ['Operation.DataOperationJobExecution.Id'], ),
                    sa.ForeignKeyConstraint(['EventId'], ['Common.OperationEvent.Id'], ),
                    sa.PrimaryKeyConstraint('Id'),
                    schema='Operation'
                    )
    op.create_table('DataOperationJobExecutionIntegration',
                    sa.Column('Id', sa.Integer(), nullable=False),
                    sa.Column('DataOperationJobExecutionId', sa.Integer(), nullable=True),
                    sa.Column('DataOperationIntegrationId', sa.Integer(), nullable=True),
                    sa.Column('StatusId', sa.Integer(), nullable=True),
                    sa.Column('StartDate', sa.DateTime(), nullable=False),
                    sa.Column('EndDate', sa.DateTime(), nullable=True),
                    sa.Column('Limit', sa.Integer(), nullable=True),
                    sa.Column('ProcessCount', sa.Integer(), nullable=True),
                    sa.Column('SourceDataCount', sa.Integer(), nullable=True),
                    sa.Column('Log', sa.String(length=1000), nullable=True),
                    sa.Column('CreatedByUserId', sa.Integer(), nullable=False),
                    sa.Column('CreationDate', sa.DateTime(), nullable=False),
                    sa.Column('LastUpdatedUserId', sa.Integer(), nullable=True),
                    sa.Column('LastUpdatedDate', sa.DateTime(), nullable=True),
                    sa.Column('IsDeleted', sa.Integer(), nullable=False),
                    sa.Column('Comments', sa.String(length=1000), nullable=True),
                    sa.Column('RowVersion', sa.TIMESTAMP(), nullable=True),
                    sa.ForeignKeyConstraint(['DataOperationIntegrationId'],
                                            ['Operation.DataOperationIntegration.Id'], ),
                    sa.ForeignKeyConstraint(['DataOperationJobExecutionId'],
                                            ['Operation.DataOperationJobExecution.Id'], ),
                    sa.ForeignKeyConstraint(['StatusId'], ['Common.Status.Id'], ),
                    sa.PrimaryKeyConstraint('Id'),
                    schema='Operation'
                    )
    op.create_table('DataOperationJobExecutionIntegrationEvent',
                    sa.Column('Id', sa.Integer(), nullable=False),
                    sa.Column('DataOperationJobExecutionIntegrationId', sa.Integer(), nullable=True),
                    sa.Column('EventId', sa.Integer(), nullable=True),
                    sa.Column('EventDate', sa.DateTime(), nullable=False),
                    sa.Column('AffectedRowCount', sa.Integer(), nullable=True),
                    sa.Column('CreatedByUserId', sa.Integer(), nullable=False),
                    sa.Column('CreationDate', sa.DateTime(), nullable=False),
                    sa.Column('LastUpdatedUserId', sa.Integer(), nullable=True),
                    sa.Column('LastUpdatedDate', sa.DateTime(), nullable=True),
                    sa.Column('IsDeleted', sa.Integer(), nullable=False),
                    sa.Column('Comments', sa.String(length=1000), nullable=True),
                    sa.Column('RowVersion', sa.TIMESTAMP(), nullable=True),
                    sa.ForeignKeyConstraint(['DataOperationJobExecutionIntegrationId'],
                                            ['Operation.DataOperationJobExecutionIntegration.Id'], ),
                    sa.ForeignKeyConstraint(['EventId'], ['Common.OperationEvent.Id'], ),
                    sa.PrimaryKeyConstraint('Id'),
                    schema='Operation'
                    )
    # ### end Alembic commands ###

    insert_connection_types()
    insert_event_datas()
    insert_statuses()
    insert_event_datas()


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('DataOperationJobExecutionIntegrationEvent', schema='Operation')
    op.drop_table('DataOperationJobExecutionIntegration', schema='Operation')
    op.drop_table('DataOperationJobExecutionEvent', schema='Operation')
    op.drop_table('DataOperationJobExecution', schema='Operation')
    op.drop_table('DataOperationJob', schema='Operation')
    op.drop_table('DataOperationIntegration', schema='Operation')
    op.drop_table('DataOperationContact', schema='Operation')
    op.drop_table('DataIntegrationExecutionJob', schema='Integration')
    op.drop_table('DataIntegrationConnection', schema='Integration')
    op.drop_table('DataIntegrationColumn', schema='Integration')
    op.drop_table('ConnectionDatabase', schema='Connection')
    op.drop_table('DataOperation', schema='Operation')
    op.drop_index(op.f('ix_Integration_DataIntegration_Code'), table_name='DataIntegration', schema='Integration')
    op.drop_table('DataIntegration', schema='Integration')
    op.drop_table('ConnectorType', schema='Connection')
    op.drop_index(op.f('ix_Connection_Connection_Name'), table_name='Connection', schema='Connection')
    op.drop_table('Connection', schema='Connection')
    op.drop_table('ApSchedulerJobEvent', schema='Aps')
    op.drop_table('Definition', schema='Operation')
    op.drop_table('ConnectionType', schema='Connection')
    op.drop_table('Status', schema='Common')
    op.drop_table('OperationEvent', schema='Common')
    op.drop_index(op.f('ix_Common_Log_TypeId'), table_name='Log', schema='Common')
    op.drop_index(op.f('ix_Common_Log_JobId'), table_name='Log', schema='Common')
    op.drop_table('Log', schema='Common')
    op.drop_table('ConfigParameter', schema='Common')
    op.drop_index(op.f('ix_Aps_ApSchedulerJobsTable_next_run_time'), table_name='ApSchedulerJobsTable', schema='Aps')
    op.drop_table('ApSchedulerJobsTable', schema='Aps')
    op.drop_table('ApSchedulerJob', schema='Aps')
    op.drop_table('ApSchedulerEvent', schema='Aps')
    # ### end Alembic commands ###
    op.execute('DROP SCHEMA "Aps"')
    op.execute('DROP SCHEMA "Connection"')
    op.execute('DROP SCHEMA "Integration"')
    op.execute('DROP SCHEMA "Operation"')
