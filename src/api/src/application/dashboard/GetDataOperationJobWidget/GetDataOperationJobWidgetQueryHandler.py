from injector import inject
from pdip.cqrs import IQueryHandler
from pdip.dependency import IScoped

from src.application.dashboard.GetDataOperationJobWidget.GetDataOperationJobWidgetMapping import \
    GetDataOperationJobWidgetMapping
from src.application.dashboard.GetDataOperationJobWidget.GetDataOperationJobWidgetQuery import \
    GetDataOperationJobWidgetQuery
from src.application.dashboard.GetDataOperationJobWidget.GetDataOperationJobWidgetResponse import \
    GetDataOperationJobWidgetResponse
from src.application.dashboard.GetDataOperationJobWidget.GetDataOperationJobWidgetSpecifications import \
    GetDataOperationJobWidgetSpecifications


class GetDataOperationJobWidgetQueryHandler(IQueryHandler[GetDataOperationJobWidgetQuery], IScoped):
    @inject
    def __init__(self,
                 specifications: GetDataOperationJobWidgetSpecifications):
        self.specifications = specifications

    def handle(self, query: GetDataOperationJobWidgetQuery) -> GetDataOperationJobWidgetResponse:
        result = GetDataOperationJobWidgetResponse()
        data_query = self.specifications.specify(query=query)
        result.Data = GetDataOperationJobWidgetMapping.to_dto(data_query)
        return result
