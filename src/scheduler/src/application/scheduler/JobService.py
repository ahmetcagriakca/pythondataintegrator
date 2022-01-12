from pdip.cqrs import Dispatcher
from pdip.dependency.container import DependencyContainer

from src.application.StartJob.StartJobCommand import StartJobCommand


class JobService:
    @staticmethod
    def job_start_data_operation(job_id, data_operation_id: int):
        command = StartJobCommand(DataOperationId=data_operation_id, JobId=job_id)
        DependencyContainer.Instance.get(Dispatcher).dispatch(command)
