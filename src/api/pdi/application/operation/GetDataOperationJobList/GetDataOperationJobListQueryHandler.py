from injector import inject
from pdip.cqrs import IQueryHandler
from pdip.data.repository import RepositoryProvider
from pdip.dependency import IScoped

from pdi.application.operation.GetDataOperationJobList.GetDataOperationJobListMapping import \
    GetDataOperationJobListMapping
from pdi.application.operation.GetDataOperationJobList.GetDataOperationJobListQuery import GetDataOperationJobListQuery
from pdi.application.operation.GetDataOperationJobList.GetDataOperationJobListResponse import \
    GetDataOperationJobListResponse
from pdi.application.operation.GetDataOperationJobList.GetDataOperationJobListSpecifications import \
    GetDataOperationJobListSpecifications
from pdi.domain.operation import DataOperationJob


class GetDataOperationJobListQueryHandler(IQueryHandler[GetDataOperationJobListQuery], IScoped):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 data_operation_job_list_specification: GetDataOperationJobListSpecifications):
        self.data_operation_job_list_specification = data_operation_job_list_specification
        self.repository_provider = repository_provider

    def handle(self, query: GetDataOperationJobListQuery) -> GetDataOperationJobListResponse:
        result = GetDataOperationJobListResponse()
        repository = self.repository_provider.get(DataOperationJob)
        data_query = repository.table

        result.Count = self.data_operation_job_list_specification.count(query=query, data_query=data_query)

        result.PageNumber = query.request.PageNumber
        result.PageSize = query.request.PageSize

        data_query = self.data_operation_job_list_specification.specify(query=query, data_query=data_query)

        result.Data = GetDataOperationJobListMapping.to_dtos(data_query)
        return result
