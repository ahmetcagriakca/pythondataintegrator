from injector import inject
from pdip.cqrs import IQueryHandler
from pdip.dependency import IScoped

from src.application.dashboard.GetDataOperationJobExecutionWidget.GetDataOperationJobExecutionWidgetMapping import \
    GetDataOperationJobExecutionWidgetMapping
from src.application.dashboard.GetDataOperationJobExecutionWidget.GetDataOperationJobExecutionWidgetQuery import \
    GetDataOperationJobExecutionWidgetQuery
from src.application.dashboard.GetDataOperationJobExecutionWidget.GetDataOperationJobExecutionWidgetResponse import \
    GetDataOperationJobExecutionWidgetResponse
from src.application.dashboard.GetDataOperationJobExecutionWidget.GetDataOperationJobExecutionWidgetSpecifications import \
    GetDataOperationJobExecutionWidgetSpecifications


class GetDataOperationJobExecutionWidgetQueryHandler(IQueryHandler[GetDataOperationJobExecutionWidgetQuery], IScoped):
    @inject
    def __init__(self,
                 specifications: GetDataOperationJobExecutionWidgetSpecifications):
        self.specifications = specifications

    def handle(self, query: GetDataOperationJobExecutionWidgetQuery) -> GetDataOperationJobExecutionWidgetResponse:
        result = GetDataOperationJobExecutionWidgetResponse()
        data_query = self.specifications.specify(query=query)
        result.Data = GetDataOperationJobExecutionWidgetMapping.to_dto(data_query)
        return result
