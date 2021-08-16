from injector import inject
from domain.operation.GetDataOperationJob.GetDataOperationJobMapping import GetDataOperationJobMapping
from domain.operation.GetDataOperationJob.GetDataOperationJobQuery import GetDataOperationJobQuery
from domain.operation.GetDataOperationJob.GetDataOperationJobResponse import GetDataOperationJobResponse
from domain.operation.GetDataOperationJob.GetDataOperationJobSpecifications import GetDataOperationJobSpecifications
from infrastructure.cqrs.IQueryHandler import IQueryHandler
from infrastructure.dependency.scopes import IScoped


class GetDataOperationJobQueryHandler(IQueryHandler[GetDataOperationJobQuery], IScoped):
    @inject
    def __init__(self,
                 specifications: GetDataOperationJobSpecifications):
        self.specifications = specifications

    def handle(self, query: GetDataOperationJobQuery) -> GetDataOperationJobResponse:
        result = GetDataOperationJobResponse()
        data_query = self.specifications.specify(query=query)
        result.Data = GetDataOperationJobMapping.to_dto(data_query.first())
        return result
