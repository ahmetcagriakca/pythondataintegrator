from injector import inject
from pdip.data.repository import RepositoryProvider
from pdip.dependency import IScoped
from pdip.exceptions import OperationalException

from src.application.connection.services.ConnectorTypeService import ConnectorTypeService
from src.domain.connection import ConnectionWebService
from src.domain.connection.Connection import Connection
from src.domain.connection.ConnectionBigData import ConnectionBigData
from src.domain.connection.ConnectionWebServiceSoap import ConnectionWebServiceSoap


class ConnectionWebServiceService(IScoped):

    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 connector_type_service: ConnectorTypeService
                 ):
        self.repository_provider = repository_provider
        self.connector_type_service = connector_type_service
        self.connection_web_service_repository = repository_provider.get(ConnectionWebService)
        self.connection_web_service_soap_repository = repository_provider.get(ConnectionWebServiceSoap)

    def create(self, connection: Connection, connector_type_id: int, ssl: bool, wsdl: str) -> ConnectionWebService:
        """
        Create BigData connection
        """
        connector_type = self.connector_type_service.get_by_id(id=connector_type_id)
        if connector_type is None:
            raise OperationalException(f"{connector_type_id} not found")
        if connector_type.ConnectionTypeId != connection.ConnectionTypeId:
            raise OperationalException(f"{connector_type_id} incompatible with {connection.ConnectionType.Name}")
        connection_web_service = ConnectionWebService(
            Connection=connection,
            ConnectorType=connector_type,
            Ssl=ssl
        )

        self.connection_web_service_repository.insert(connection_web_service)

        connection_web_service_soap = ConnectionWebServiceSoap(
            ConnectionWebService=connection_web_service,
            Wsdl=wsdl
        )
        self.connection_web_service_soap_repository.insert(connection_web_service_soap)
        return connection_web_service_soap

    def update(self, connection: Connection, connector_type_id: int, ssl: bool, wsdl: str) -> ConnectionBigData:
        """
        Update BigData connection
        """

        connection_web_service = self.connection_web_service_repository.first(ConnectionId=connection.Id)

        connector_type = self.connector_type_service.get_by_id(id=connector_type_id)
        if connector_type is None:
            raise OperationalException(f"{connector_type_id} not found")
        if connector_type.ConnectionTypeId != connection.ConnectionTypeId:
            raise OperationalException(f"{connector_type_id} incompatible with {connection.ConnectionType.Name}")
        connection_web_service.ConnectorType = connector_type
        connection_web_service.Ssl = ssl

        connection_web_service_soap = self.connection_web_service_soap_repository.first(
            ConnectionWebServiceId=connection_web_service.Id)
        connection_web_service_soap.Wsdl = wsdl
        return connection_web_service

    def delete(self, id: int):
        """
        Delete BigData connection
        """
        connection_web_service_soap = self.connection_web_service_soap_repository.first(
            ConnectionWebServiceId=id)
        self.connection_web_service_soap_repository.delete_by_id(connection_web_service_soap.Id)
        self.connection_web_service_repository.delete_by_id(id)
