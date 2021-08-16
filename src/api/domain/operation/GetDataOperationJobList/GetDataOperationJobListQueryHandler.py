from injector import inject
from domain.operation.GetDataOperationJobList.GetDataOperationJobListMapping import GetDataOperationJobListMapping
from domain.operation.GetDataOperationJobList.GetDataOperationJobListQuery import GetDataOperationJobListQuery
from domain.operation.GetDataOperationJobList.GetDataOperationJobListResponse import GetDataOperationJobListResponse
from domain.operation.GetDataOperationJobList.GetDataOperationJobListSpecifications import \
    GetDataOperationJobListSpecifications
from infrastructure.cqrs.IQueryHandler import IQueryHandler
from infrastructure.data.RepositoryProvider import RepositoryProvider
from infrastructure.dependency.scopes import IScoped
from models.dao.operation import DataOperationJob


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
