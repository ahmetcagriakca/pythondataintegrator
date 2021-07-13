from injector import inject
from domain.operation.GetDataOperationList.DataOperationListMapping import DataOperationListMapping
from domain.operation.GetDataOperationList.DataOperationListQuery import DataOperationListQuery
from domain.operation.GetDataOperationList.DataOperationListResponse import DataOperationListResponse
from domain.operation.GetDataOperationList.DataOperationListSpecifications import DataOperationListSpecifications
from infrastructor.data.RepositoryProvider import RepositoryProvider
from models.dao.operation import DataOperation


class DataOperationListQueryHandler:
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 data_operation_list_specification: DataOperationListSpecifications):
        self.data_operation_list_specification = data_operation_list_specification
        self.repository_provider = repository_provider

    def handle(self, query: DataOperationListQuery) -> DataOperationListResponse:
        result = DataOperationListResponse()
        repository = self.repository_provider.get(DataOperation)
        data_query = repository.table \

        result.Count = self.data_operation_list_specification.count(query=query, data_query=data_query)

        data_query = self.data_operation_list_specification.specify(query=query, data_query=data_query)

        result.PageNumber = query.request.PageNumber
        result.PageSize = query.request.PageSize

        result.PageData = DataOperationListMapping.to_dtos(data_query)
        return result
