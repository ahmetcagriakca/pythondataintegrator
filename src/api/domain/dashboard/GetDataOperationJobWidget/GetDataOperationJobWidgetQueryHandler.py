from injector import inject
from domain.dashboard.GetDataOperationJobWidget.GetDataOperationJobWidgetMapping import GetDataOperationJobWidgetMapping
from domain.dashboard.GetDataOperationJobWidget.GetDataOperationJobWidgetQuery import GetDataOperationJobWidgetQuery
from domain.dashboard.GetDataOperationJobWidget.GetDataOperationJobWidgetResponse import GetDataOperationJobWidgetResponse
from domain.dashboard.GetDataOperationJobWidget.GetDataOperationJobWidgetSpecifications import GetDataOperationJobWidgetSpecifications
from pdip.cqrs import IQueryHandler 
from pdip.dependency import IScoped


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
