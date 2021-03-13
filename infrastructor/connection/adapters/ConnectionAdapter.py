from abc import abstractmethod
from typing import List

from models.dto.LimitModifier import LimitModifier


class ConnectionAdapter:
    @abstractmethod
    def clear_data(self):
        pass

    @abstractmethod
    def get_source_data_count(self, data_integration_id):
        pass

    @abstractmethod
    def get_source_data(self, data_integration_id: int, limit_modifier: LimitModifier) -> List[any]:
        pass

    @abstractmethod
    def prepare_data(self, data_integration_id: int, source_data: List[any]) -> List[any]:
        pass

    @abstractmethod
    def write_target_data(self, data_integration_id: int, prepared_data: List[any], ) -> int:
        pass

    @abstractmethod
    def do_target_operation(self, data_integration_id: int) -> int:
        pass
