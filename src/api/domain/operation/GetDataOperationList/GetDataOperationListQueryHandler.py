from injector import inject
from domain.operation.GetDataOperationList.GetDataOperationListMapping import GetDataOperationListMapping
from domain.operation.GetDataOperationList.GetDataOperationListQuery import GetDataOperationListQuery
from domain.operation.GetDataOperationList.GetDataOperationListResponse import GetDataOperationListResponse
from domain.operation.GetDataOperationList.GetDataOperationListSpecifications import GetDataOperationListSpecifications
from infrastructure.data.RepositoryProvider import RepositoryProvider
from models.dao.operation import DataOperation


class GetDataOperationListQueryHandler:
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 data_operation_list_specification: GetDataOperationListSpecifications):
        self.data_operation_list_specification = data_operation_list_specification
        self.repository_provider = repository_provider

    def handle(self, query: GetDataOperationListQuery) -> GetDataOperationListResponse:
        result = GetDataOperationListResponse()
        repository = self.repository_provider.get(DataOperation)
        data_query = repository.table \

        result.Count = self.data_operation_list_specification.count(query=query, data_query=data_query)

        data_query = self.data_operation_list_specification.specify(query=query, data_query=data_query)

        result.PageNumber = query.request.PageNumber
        result.PageSize = query.request.PageSize

        result.Data = GetDataOperationListMapping.to_dtos(data_query)
        return result
