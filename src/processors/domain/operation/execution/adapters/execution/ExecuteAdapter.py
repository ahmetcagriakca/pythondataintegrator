from abc import ABC, abstractmethod


class ExecuteAdapter(ABC):

    @abstractmethod
    def execute(self,
                data_operation_integration_id: int,
                data_operation_job_execution_id: int,
                data_operation_job_execution_integration_id: int):
        pass

    @abstractmethod
    def get_start_log(self, data_integration_id: int):
        pass

    @abstractmethod
    def get_finish_log(self, data_integration_id: int, data_count: int):
        pass

    @abstractmethod
    def get_error_log(self, data_integration_id: int):
        pass

    @abstractmethod
    def check_error_raise(self) -> bool:
        pass
