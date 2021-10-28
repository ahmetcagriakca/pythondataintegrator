from abc import ABC, abstractmethod

from injector import inject
from pdip.dependency import IScoped


class ExecuteIntegrationStrategy(ABC, IScoped):
    @inject
    def __init__(self):
        pass

    @abstractmethod
    def execute(self,
                data_operation_job_execution_id: int,
                data_operation_job_execution_integration_id: int,
                data_operation_integration_id: int) -> int:
        pass
