from injector import inject
from domain.dashboard.GetDataOperationJobExecutionWidget.GetDataOperationJobExecutionWidgetMapping import GetDataOperationJobExecutionWidgetMapping
from domain.dashboard.GetDataOperationJobExecutionWidget.GetDataOperationJobExecutionWidgetQuery import GetDataOperationJobExecutionWidgetQuery
from domain.dashboard.GetDataOperationJobExecutionWidget.GetDataOperationJobExecutionWidgetResponse import GetDataOperationJobExecutionWidgetResponse
from domain.dashboard.GetDataOperationJobExecutionWidget.GetDataOperationJobExecutionWidgetSpecifications import GetDataOperationJobExecutionWidgetSpecifications
from pdip.cqrs import IQueryHandler 
from pdip.dependency import IScoped


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
