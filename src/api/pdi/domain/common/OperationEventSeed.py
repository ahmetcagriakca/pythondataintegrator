from pdip.data.repository import RepositoryProvider
from pdip.dependency.container import DependencyContainer
from pdip.logging.loggers.sql import SqlLogger

from pdip.data.seed import Seed
from pdi.domain.common.OperationEvent import OperationEvent
from pdi.domain.enums.events import EVENT_EXECUTION_INITIALIZED, EVENT_EXECUTION_FINISHED, EVENT_EXECUTION_STARTED, \
    EVENT_EXECUTION_INTEGRATION_INITIALIZED, EVENT_EXECUTION_INTEGRATION_STARTED, \
    EVENT_EXECUTION_INTEGRATION_GET_SOURCE_DATA_COUNT, \
    EVENT_EXECUTION_INTEGRATION_EXECUTE_TRUNCATE, \
    EVENT_EXECUTION_INTEGRATION_EXECUTE_QUERY, EVENT_EXECUTION_INTEGRATION_EXECUTE_OPERATION, \
    EVENT_EXECUTION_INTEGRATION_FINISHED


class OperationEventSeed(Seed):
    def seed(self):
        try:
            repository_provider = DependencyContainer.Instance.get(RepositoryProvider)
            operation_event_repository = repository_provider.get(OperationEvent)
            check_count = operation_event_repository.table.count()
            if check_count is None or check_count == 0:
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
                        "Code": EVENT_EXECUTION_INTEGRATION_INITIALIZED,
                        "Name": "EVENT_EXECUTION_INTEGRATION_INITIALIZED",
                        "Description": "Execution integration initialized",
                        "Class": "DataOperationJobExecutionIntegration"
                    },
                    {
                        "Code": EVENT_EXECUTION_INTEGRATION_STARTED,
                        "Name": "EVENT_EXECUTION_INTEGRATION_STARTED",
                        "Description": "Execution integration started",
                        "Class": "DataOperationJobExecutionIntegration"
                    },
                    {
                        "Code": EVENT_EXECUTION_INTEGRATION_GET_SOURCE_DATA_COUNT,
                        "Name": "EVENT_EXECUTION_INTEGRATION_GET_SOURCE_DATA_COUNT",
                        "Description": "Execution integration get source data count",
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
                    },
                    {
                        "Code": EVENT_EXECUTION_INTEGRATION_FINISHED,
                        "Name": "EVENT_EXECUTION_INTEGRATION_FINISHED",
                        "Description": "Execution integration finished",
                        "Class": "DataOperationJobExecutionIntegration"
                    }
                ]
                for eventJson in events_list:
                    event = OperationEvent(Code=eventJson["Code"], Name=eventJson["Name"],
                                           Description=eventJson["Description"],
                                           Class=eventJson["Class"])
                    operation_event_repository.insert(event)
                    repository_provider.commit()
        except Exception as ex:
            logger = DependencyContainer.Instance.get(SqlLogger)
            logger.exception(ex, "ApScheduler seeds getting error")
        finally:
            repository_provider.close()
