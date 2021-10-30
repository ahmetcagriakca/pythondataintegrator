from injector import inject
from pdip.cqrs import IQueryHandler
from pdip.dependency import IScoped

from pdi.application.dashboard.GetDataOperationJobWidget.GetDataOperationJobWidgetMapping import \
    GetDataOperationJobWidgetMapping
from pdi.application.dashboard.GetDataOperationJobWidget.GetDataOperationJobWidgetQuery import \
    GetDataOperationJobWidgetQuery
from pdi.application.dashboard.GetDataOperationJobWidget.GetDataOperationJobWidgetResponse import \
    GetDataOperationJobWidgetResponse
from pdi.application.dashboard.GetDataOperationJobWidget.GetDataOperationJobWidgetSpecifications import \
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
