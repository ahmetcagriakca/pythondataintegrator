from injector import inject
from domain.dashboard.GetConnectionWidget.GetConnectionWidgetMapping import GetConnectionWidgetMapping
from domain.dashboard.GetConnectionWidget.GetConnectionWidgetQuery import GetConnectionWidgetQuery
from domain.dashboard.GetConnectionWidget.GetConnectionWidgetResponse import GetConnectionWidgetResponse
from domain.dashboard.GetConnectionWidget.GetConnectionWidgetSpecifications import GetConnectionWidgetSpecifications
from pdip.cqrs import IQueryHandler 
from pdip.dependency import IScoped


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
