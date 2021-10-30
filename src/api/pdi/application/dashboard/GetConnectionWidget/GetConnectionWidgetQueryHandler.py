from injector import inject
from pdip.cqrs import IQueryHandler
from pdip.dependency import IScoped

from pdi.application.dashboard.GetConnectionWidget.GetConnectionWidgetMapping import GetConnectionWidgetMapping
from pdi.application.dashboard.GetConnectionWidget.GetConnectionWidgetQuery import GetConnectionWidgetQuery
from pdi.application.dashboard.GetConnectionWidget.GetConnectionWidgetResponse import GetConnectionWidgetResponse
from pdi.application.dashboard.GetConnectionWidget.GetConnectionWidgetSpecifications import \
    GetConnectionWidgetSpecifications


class GetConnectionWidgetQueryHandler(IQueryHandler[GetConnectionWidgetQuery], IScoped):
    @inject
    def __init__(self,
                 specifications: GetConnectionWidgetSpecifications):
        self.specifications = specifications

    def handle(self, query: GetConnectionWidgetQuery) -> GetConnectionWidgetResponse:
        result = GetConnectionWidgetResponse()
        data_query = self.specifications.specify(query=query)
        result.Data = GetConnectionWidgetMapping.to_dto(data_query)
        return result
