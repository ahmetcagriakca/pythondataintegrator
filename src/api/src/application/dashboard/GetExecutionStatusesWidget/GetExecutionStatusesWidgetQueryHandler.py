from injector import inject
from pdip.cqrs import IQueryHandler
from pdip.dependency import IScoped

from src.application.dashboard.GetExecutionStatusesWidget.GetExecutionStatusesWidgetMapping import \
    GetExecutionStatusesWidgetMapping
from src.application.dashboard.GetExecutionStatusesWidget.GetExecutionStatusesWidgetQuery import \
    GetExecutionStatusesWidgetQuery
from src.application.dashboard.GetExecutionStatusesWidget.GetExecutionStatusesWidgetResponse import \
    GetExecutionStatusesWidgetResponse
from src.application.dashboard.GetExecutionStatusesWidget.GetExecutionStatusesWidgetSpecifications import \
    GetExecutionStatusesWidgetSpecifications


class GetExecutionStatusesWidgetQueryHandler(IQueryHandler[GetExecutionStatusesWidgetQuery], IScoped):
    @inject
    def __init__(self,
                 specifications: GetExecutionStatusesWidgetSpecifications):
        self.specifications = specifications

    def handle(self, query: GetExecutionStatusesWidgetQuery) -> GetExecutionStatusesWidgetResponse:
        result = GetExecutionStatusesWidgetResponse()
        data_query = self.specifications.specify(query=query)
        result.Data = GetExecutionStatusesWidgetMapping.to_dto(data_query)
        return result
