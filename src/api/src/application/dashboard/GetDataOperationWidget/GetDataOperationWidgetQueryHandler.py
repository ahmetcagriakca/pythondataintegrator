from injector import inject
from pdip.cqrs import IQueryHandler
from pdip.dependency import IScoped

from src.application.dashboard.GetDataOperationWidget.GetDataOperationWidgetMapping import GetDataOperationWidgetMapping
from src.application.dashboard.GetDataOperationWidget.GetDataOperationWidgetQuery import GetDataOperationWidgetQuery
from src.application.dashboard.GetDataOperationWidget.GetDataOperationWidgetResponse import \
    GetDataOperationWidgetResponse
from src.application.dashboard.GetDataOperationWidget.GetDataOperationWidgetSpecifications import \
    GetDataOperationWidgetSpecifications


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
