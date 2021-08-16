from injector import inject
from domain.operation.GetDataOperationJobExecutionIntegrationList.GetDataOperationJobExecutionIntegrationListMapping import GetDataOperationJobExecutionIntegrationListMapping
from domain.operation.GetDataOperationJobExecutionIntegrationList.GetDataOperationJobExecutionIntegrationListQuery import GetDataOperationJobExecutionIntegrationListQuery
from domain.operation.GetDataOperationJobExecutionIntegrationList.GetDataOperationJobExecutionIntegrationListResponse import GetDataOperationJobExecutionIntegrationListResponse
from domain.operation.GetDataOperationJobExecutionIntegrationList.GetDataOperationJobExecutionIntegrationListSpecifications import GetDataOperationJobExecutionIntegrationListSpecifications
from infrastructure.cqrs.IQueryHandler import IQueryHandler
from infrastructure.data.RepositoryProvider import RepositoryProvider
from infrastructure.dependency.scopes import IScoped
from models.dao.operation.DataOperationJobExecutionIntegration import DataOperationJobExecutionIntegration


class GetDataOperationJobExecutionIntegrationListQueryHandler(IQueryHandler[GetDataOperationJobExecutionIntegrationListQuery], IScoped):
    @inject
    def __init__(self,
                 specifications: GetDataOperationJobExecutionIntegrationListSpecifications):
        self.specifications = specifications

    def handle(self, query: GetDataOperationJobExecutionIntegrationListQuery) -> GetDataOperationJobExecutionIntegrationListResponse:
        result = GetDataOperationJobExecutionIntegrationListResponse()
        data_query = self.specifications.specify(query=query)
        result.Data = GetDataOperationJobExecutionIntegrationListMapping.to_dtos(data_query)
        return result
