from abc import abstractmethod
from infrastructor.dependency.scopes import IScoped


class ConnectorStrategy(IScoped):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    def execute_many(self,query,data):
        pass