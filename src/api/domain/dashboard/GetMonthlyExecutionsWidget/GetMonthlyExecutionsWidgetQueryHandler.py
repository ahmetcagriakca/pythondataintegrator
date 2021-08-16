from injector import inject
from domain.dashboard.GetMonthlyExecutionsWidget.GetMonthlyExecutionsWidgetMapping import GetMonthlyExecutionsWidgetMapping
from domain.dashboard.GetMonthlyExecutionsWidget.GetMonthlyExecutionsWidgetQuery import GetMonthlyExecutionsWidgetQuery
from domain.dashboard.GetMonthlyExecutionsWidget.GetMonthlyExecutionsWidgetResponse import GetMonthlyExecutionsWidgetResponse
from domain.dashboard.GetMonthlyExecutionsWidget.GetMonthlyExecutionsWidgetSpecifications import GetMonthlyExecutionsWidgetSpecifications
from infrastructure.cqrs.IQueryHandler import IQueryHandler
from infrastructure.dependency.scopes import IScoped


class GetMonthlyExecutionsWidgetQueryHandler(IQueryHandler[GetMonthlyExecutionsWidgetQuery], IScoped):
    @inject
    def __init__(self,
                 specifications: GetMonthlyExecutionsWidgetSpecifications):
        self.specifications = specifications

    def handle(self, query: GetMonthlyExecutionsWidgetQuery) -> GetMonthlyExecutionsWidgetResponse:
        result = GetMonthlyExecutionsWidgetResponse()
        data_query = self.specifications.specify(query=query)
        result.Data = GetMonthlyExecutionsWidgetMapping.to_dto(data_query)
        return result
