from abc import abstractmethod
from queue import Queue
from typing import List

from pandas import DataFrame

from models.dto.PagingModifier import PagingModifier


class ConnectionAdapter:
    @abstractmethod
    def clear_data(self):
        pass

    @abstractmethod
    def get_source_data_count(self, data_integration_id):
        pass

    @abstractmethod
    def get_source_data(self, data_integration_id: int, paging_modifier: PagingModifier) -> List[any]:
        pass

    @abstractmethod
    def prepare_data(self, data_integration_id: int, source_data: DataFrame) -> List[any]:
        pass

    @abstractmethod
    def write_target_data(self, data_integration_id: int, prepared_data: List[any], ) -> int:
        pass

    @abstractmethod
    def do_target_operation(self, data_integration_id: int) -> int:
        pass

    @abstractmethod
    def start_source_data_operation(self,
                                    data_integration_id: int,
                                    data_operation_job_execution_integration_id: int,
                                    limit: int,
                                    process_count: int,
                                    data_queue: Queue,
                                    data_result_queue: Queue):
        pass
