from injector import inject

from domain.common.lookup.LookupDto import LookupDto
from domain.common.lookup.LookupResponse import LookupResponse
from infrastructor.data.RepositoryProvider import RepositoryProvider
from infrastructor.dependency.scopes import IScoped
from models.dao.connection import ConnectionType, ConnectorType
from models.dao.connection.Connection import Connection


class ConnectionLookupService(IScoped):

    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 ):
        self.repository_provider = repository_provider
        self.connection_repository = repository_provider.get(Connection)
        self.connection_type_repository = repository_provider.get(ConnectionType)
        self.connector_type_repository = repository_provider.get(ConnectorType)

    def get_connection_names(self) -> LookupResponse:
        """
        """
        entities = self.connection_repository.filter_by(IsDeleted=0).all()
        lookup_datas = [LookupDto(Id=entity.Id, Name=entity.Name) for entity in entities]
        response = LookupResponse(datas=lookup_datas)
        return response

    def get_connection_type_names(self) -> LookupResponse:
        """
        """
        entities = self.connection_type_repository.filter_by(IsDeleted=0).all()
        lookup_datas = [LookupDto(Id=entity.Id, Name=entity.Name) for entity in entities]
        response = LookupResponse(datas=lookup_datas)
        return response

    def get_connector_type_names(self) -> LookupResponse:
        """
        """
        entities = self.connector_type_repository.filter_by(IsDeleted=0).all()
        lookup_datas = [LookupDto(Id=entity.Id, Name=entity.Name) for entity in entities]
        response = LookupResponse(datas=lookup_datas)
        return response
