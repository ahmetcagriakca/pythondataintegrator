from injector import inject
from pdip.cqrs import IQueryHandler
from pdip.dependency import IScoped

from pdi.application.operation.GetDataOperationJobExecutionIntegrationList.GetDataOperationJobExecutionIntegrationListMapping import \
    GetDataOperationJobExecutionIntegrationListMapping
from pdi.application.operation.GetDataOperationJobExecutionIntegrationList.GetDataOperationJobExecutionIntegrationListQuery import \
    GetDataOperationJobExecutionIntegrationListQuery
from pdi.application.operation.GetDataOperationJobExecutionIntegrationList.GetDataOperationJobExecutionIntegrationListResponse import \
    GetDataOperationJobExecutionIntegrationListResponse
from pdi.application.operation.GetDataOperationJobExecutionIntegrationList.GetDataOperationJobExecutionIntegrationListSpecifications import \
    GetDataOperationJobExecutionIntegrationListSpecifications


class GetDataOperationJobExecutionIntegrationListQueryHandler(
    IQueryHandler[GetDataOperationJobExecutionIntegrationListQuery], IScoped):
    @inject
    def __init__(self,
                 specifications: GetDataOperationJobExecutionIntegrationListSpecifications):
        self.specifications = specifications

    def handle(self,
               query: GetDataOperationJobExecutionIntegrationListQuery) -> GetDataOperationJobExecutionIntegrationListResponse:
        result = GetDataOperationJobExecutionIntegrationListResponse()
        data_query = self.specifications.specify(query=query)
        result.Data = GetDataOperationJobExecutionIntegrationListMapping.to_dtos(data_query)
        return result
