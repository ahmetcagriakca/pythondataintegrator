from typing import List

from injector import inject
from pdip.data.repository import RepositoryProvider
from pdip.dependency import IScoped
from pdip.exceptions import OperationalException

from src.domain.connection.ConnectorType import ConnectorType


class ConnectorTypeService(IScoped):

    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 ):
        self.repository_provider = repository_provider
        self.connector_type_repository = repository_provider.get(ConnectorType)

    def get(self) -> List[ConnectorType]:
        """
        Get all
        """
        entities = self.connector_type_repository.filter_by(IsDeleted=0).all()
        return entities

    def get_by_name(self, name) -> ConnectorType:
        """
        Get
        """
        entity = self.connector_type_repository.first(IsDeleted=0, Name=name)
        if entity is None:
            raise OperationalException(f"{name} Connector Type Not Found")
        return entity

    def get_by_id(self, id: int) -> ConnectorType:
        """
        Get
        """
        entity = self.connector_type_repository.first(IsDeleted=0, Id=id)
        if entity is None:
            raise OperationalException(f"{id} Connector Type Not Found")
        return entity
