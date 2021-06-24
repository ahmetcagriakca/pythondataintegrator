
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


def start():
    from IocManager import IocManager

    from scheduler.JobScheduler import JobScheduler
    from rpc.SchedulerService import SchedulerService

    IocManager.set_job_scheduler(job_scheduler=JobScheduler)
    IocManager.set_scheduler_service(scheduler_service=SchedulerService)
    IocManager.initialize()
    IocManager.run()


if __name__ == "__main__":
    start()
