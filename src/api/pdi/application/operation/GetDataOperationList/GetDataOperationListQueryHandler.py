from injector import inject
from pdip.cqrs import IQueryHandler
from pdip.data.repository import RepositoryProvider
from pdip.dependency import IScoped

from pdi.application.operation.GetDataOperationList.GetDataOperationListMapping import GetDataOperationListMapping
from pdi.application.operation.GetDataOperationList.GetDataOperationListQuery import GetDataOperationListQuery
from pdi.application.operation.GetDataOperationList.GetDataOperationListResponse import GetDataOperationListResponse
from pdi.application.operation.GetDataOperationList.GetDataOperationListSpecifications import \
    GetDataOperationListSpecifications
from pdi.domain.operation import DataOperation


class GetDataOperationListQueryHandler(IQueryHandler[GetDataOperationListQuery], IScoped):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 data_operation_list_specification: GetDataOperationListSpecifications):
        self.data_operation_list_specification = data_operation_list_specification
        self.repository_provider = repository_provider

    def handle(self, query: GetDataOperationListQuery) -> GetDataOperationListResponse:
        result = GetDataOperationListResponse()
        repository = self.repository_provider.get(DataOperation)
        data_query = repository.table
        result.Count = self.data_operation_list_specification.count(query=query, data_query=data_query)

        data_query = self.data_operation_list_specification.specify(query=query, data_query=data_query)

        result.PageNumber = query.request.PageNumber
        result.PageSize = query.request.PageSize

        result.Data = GetDataOperationListMapping.to_dtos(data_query)
        return result
