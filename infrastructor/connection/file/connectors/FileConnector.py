from abc import abstractmethod
from infrastructor.dependency.scopes import IScoped

from pandas import DataFrame


class FileConnector(IScoped):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def get_data_count(self, file: str):
        pass

    @abstractmethod
    def read_data(self, file: str, names: [], start: int, limit: int,
                  header: int, separator: str) -> DataFrame:
        pass

    def write_data(self, file: str, data: DataFrame, separator: str):
        pass

    def recreate_file(self, file: str, headers: [], separator: str):
        pass

    def delete_file(self, file: str):
        pass
