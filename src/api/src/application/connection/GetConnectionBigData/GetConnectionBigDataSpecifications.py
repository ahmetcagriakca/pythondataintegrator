from injector import inject
from pdip.data.repository import RepositoryProvider
from pdip.dependency import IScoped
from sqlalchemy import or_
from sqlalchemy.orm import Query

from src.application.connection.GetConnectionBigData.GetConnectionBigDataQuery import GetConnectionBigDataQuery
from src.domain.connection import ConnectionType, ConnectorType, Connection, ConnectionServer, \
    ConnectionBigData, ConnectionSecret
from src.domain.secret import Secret, SecretSource, AuthenticationType, SecretSourceBasicAuthentication, \
    SecretSourceKerberosAuthentication


class GetConnectionBigDataSpecifications(IScoped):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider
                 ):
        self.repository_provider = repository_provider

    def __specified_query(self, query: GetConnectionBigDataQuery) -> Query:
        repository = self.repository_provider.get(Connection)
        data_query = repository.table
        specified_query = data_query \
            .join(ConnectionType, ConnectionType.Id == Connection.ConnectionTypeId) \
            .join(ConnectionServer, ConnectionServer.ConnectionId == Connection.Id) \
            .join(ConnectionSecret, ConnectionSecret.ConnectionId == Connection.Id) \
            .join(Secret, Secret.Id == ConnectionSecret.SecretId) \
            .join(SecretSource, SecretSource.SecretId == Secret.Id) \
            .join(AuthenticationType, AuthenticationType.Id == SecretSource.AuthenticationTypeId) \
            .join(SecretSourceBasicAuthentication,
                  SecretSourceBasicAuthentication.SecretSourceId == SecretSource.Id, isouter=True) \
            .join(SecretSourceKerberosAuthentication,
                  SecretSourceKerberosAuthentication.SecretSourceId == SecretSource.Id, isouter=True) \
            .join(ConnectionBigData, ConnectionBigData.ConnectionId == Connection.Id) \
            .join(ConnectorType, ConnectorType.Id == ConnectionBigData.ConnectorTypeId)
        specified_query = specified_query.filter(Connection.Id == query.request.Id)
        return specified_query

    def specify(self, query: GetConnectionBigDataQuery) -> Query:
        data_query = self.__specified_query(query=query)
        return data_query

    def count(self, query: GetConnectionBigDataQuery) -> Query:
        return self.__specified_query(query=query).count()
