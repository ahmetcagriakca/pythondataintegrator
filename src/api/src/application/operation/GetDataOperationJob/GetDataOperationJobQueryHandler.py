from injector import inject
from pdip.cqrs import IQueryHandler
from pdip.dependency import IScoped

from src.application.operation.GetDataOperationJob.GetDataOperationJobMapping import GetDataOperationJobMapping
from src.application.operation.GetDataOperationJob.GetDataOperationJobQuery import GetDataOperationJobQuery
from src.application.operation.GetDataOperationJob.GetDataOperationJobResponse import GetDataOperationJobResponse
from src.application.operation.GetDataOperationJob.GetDataOperationJobSpecifications import \
    GetDataOperationJobSpecifications


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
