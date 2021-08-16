from injector import inject
from domain.dashboard.GetDataOperationWidget.GetDataOperationWidgetMapping import GetDataOperationWidgetMapping
from domain.dashboard.GetDataOperationWidget.GetDataOperationWidgetQuery import GetDataOperationWidgetQuery
from domain.dashboard.GetDataOperationWidget.GetDataOperationWidgetResponse import GetDataOperationWidgetResponse
from domain.dashboard.GetDataOperationWidget.GetDataOperationWidgetSpecifications import GetDataOperationWidgetSpecifications
from infrastructure.cqrs.IQueryHandler import IQueryHandler
from infrastructure.dependency.scopes import IScoped


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
