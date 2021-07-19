from injector import inject
from domain.connection.LookupConnectorType.LookupConnectorTypeMapping import LookupConnectorTypeMapping
from domain.connection.LookupConnectorType.LookupConnectorTypeQuery import LookupConnectorTypeQuery
from domain.connection.LookupConnectorType.LookupConnectorTypeResponse import LookupConnectorTypeResponse
from domain.connection.LookupConnectorType.LookupConnectorTypeSpecifications import LookupConnectorTypeSpecifications
from infrastructure.cqrs.IQueryHandler import IQueryHandler
from infrastructure.data.RepositoryProvider import RepositoryProvider
from infrastructure.dependency.scopes import IScoped
from models.dao.connection.ConnectorType import ConnectorType


class LookupConnectorTypeQueryHandler(IQueryHandler[LookupConnectorTypeQuery], IScoped):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 specifications: LookupConnectorTypeSpecifications):
        self.repository_provider = repository_provider
        self.specifications = specifications

    def handle(self, query: LookupConnectorTypeQuery) -> LookupConnectorTypeResponse:
        result = LookupConnectorTypeResponse()
        repository = self.repository_provider.get(ConnectorType)
        data_query = repository.table
        data_query = self.specifications.specify(query=query, data_query=data_query)
        result.Data = LookupConnectorTypeMapping.to_dtos(data_query)
        return result
