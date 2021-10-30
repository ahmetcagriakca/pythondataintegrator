from injector import inject
from pdip.cqrs import IQueryHandler
from pdip.dependency import IScoped

from pdi.application.dashboard.GetMonthlyExecutionsWidget.GetMonthlyExecutionsWidgetMapping import \
    GetMonthlyExecutionsWidgetMapping
from pdi.application.dashboard.GetMonthlyExecutionsWidget.GetMonthlyExecutionsWidgetQuery import \
    GetMonthlyExecutionsWidgetQuery
from pdi.application.dashboard.GetMonthlyExecutionsWidget.GetMonthlyExecutionsWidgetResponse import \
    GetMonthlyExecutionsWidgetResponse
from pdi.application.dashboard.GetMonthlyExecutionsWidget.GetMonthlyExecutionsWidgetSpecifications import \
    GetMonthlyExecutionsWidgetSpecifications


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
