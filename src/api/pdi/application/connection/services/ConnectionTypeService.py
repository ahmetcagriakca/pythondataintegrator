from typing import List

from injector import inject
from pdip.data import RepositoryProvider
from pdip.dependency import IScoped
from pdip.exceptions import OperationalException

from pdi.domain.connection.ConnectionType import ConnectionType


class ConnectionTypeService(IScoped):

    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 ):
        self.repository_provider = repository_provider
        self.connection_type_repository = repository_provider.get(ConnectionType)

    def get(self) -> List[ConnectionType]:
        """
        Get all
        """
        entities = self.connection_type_repository.filter_by(IsDeleted=0).all()
        return entities

    def get_by_name(self, name) -> ConnectionType:
        """
        Get
        """
        entity = self.connection_type_repository.first(IsDeleted=0, Name=name)
        if entity is None:
            raise OperationalException("Connection Type Not Found")
        return entity
