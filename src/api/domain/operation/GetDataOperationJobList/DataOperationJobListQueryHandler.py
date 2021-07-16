from injector import inject
from domain.operation.GetDataOperationJobList.DataOperationJobListMapping import DataOperationJobListMapping
from domain.operation.GetDataOperationJobList.DataOperationJobListQuery import DataOperationJobListQuery
from domain.operation.GetDataOperationJobList.DataOperationJobListResponse import DataOperationJobListResponse
from domain.operation.GetDataOperationJobList.DataOperationJobListSpecifications import \
    DataOperationJobListSpecifications
from infrastructure.data.RepositoryProvider import RepositoryProvider
from models.dao.operation import DataOperationJob


class DataOperationJobListQueryHandler:
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 data_operation_job_list_specification: DataOperationJobListSpecifications):
        self.data_operation_job_list_specification = data_operation_job_list_specification
        self.repository_provider = repository_provider

    def handle(self, query: DataOperationJobListQuery) -> DataOperationJobListResponse:
        result = DataOperationJobListResponse()
        repository = self.repository_provider.get(DataOperationJob)
        data_query = repository.table

        result.Count = self.data_operation_job_list_specification.count(query=query, data_query=data_query)

        data_query = self.data_operation_job_list_specification.specify(query=query, data_query=data_query)

        result.PageNumber = query.request.PageNumber
        result.PageSize = query.request.PageSize

        result.PageData = DataOperationJobListMapping.to_dtos(data_query)
        return result
