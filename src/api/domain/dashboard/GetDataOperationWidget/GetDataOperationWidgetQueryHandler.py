from injector import inject
from domain.dashboard.GetDataOperationWidget.GetDataOperationWidgetMapping import GetDataOperationWidgetMapping
from domain.dashboard.GetDataOperationWidget.GetDataOperationWidgetQuery import GetDataOperationWidgetQuery
from domain.dashboard.GetDataOperationWidget.GetDataOperationWidgetResponse import GetDataOperationWidgetResponse
from domain.dashboard.GetDataOperationWidget.GetDataOperationWidgetSpecifications import GetDataOperationWidgetSpecifications
from pdip.cqrs import IQueryHandler 
from pdip.dependency import IScoped


class GetDataOperationWidgetQueryHandler(IQueryHandler[GetDataOperationWidgetQuery], IScoped):
    @inject
    def __init__(self,
                 specifications: GetDataOperationWidgetSpecifications):
        self.specifications = specifications

    def handle(self, query: GetDataOperationWidgetQuery) -> GetDataOperationWidgetResponse:
        result = GetDataOperationWidgetResponse()
        data_query = self.specifications.specify(query=query)
        result.Data = GetDataOperationWidgetMapping.to_dto(data_query)
        return result
