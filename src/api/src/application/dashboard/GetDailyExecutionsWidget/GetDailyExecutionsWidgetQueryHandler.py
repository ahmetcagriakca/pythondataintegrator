from injector import inject
from pdip.cqrs import IQueryHandler
from pdip.dependency import IScoped

from src.application.dashboard.GetDailyExecutionsWidget.GetDailyExecutionsWidgetMapping import \
    GetDailyExecutionsWidgetMapping
from src.application.dashboard.GetDailyExecutionsWidget.GetDailyExecutionsWidgetQuery import \
    GetDailyExecutionsWidgetQuery
from src.application.dashboard.GetDailyExecutionsWidget.GetDailyExecutionsWidgetResponse import \
    GetDailyExecutionsWidgetResponse
from src.application.dashboard.GetDailyExecutionsWidget.GetDailyExecutionsWidgetSpecifications import \
    GetDailyExecutionsWidgetSpecifications


class GetDailyExecutionsWidgetQueryHandler(IQueryHandler[GetDailyExecutionsWidgetQuery], IScoped):
    @inject
    def __init__(self,
                 specifications: GetDailyExecutionsWidgetSpecifications):
        self.specifications = specifications

    def handle(self, query: GetDailyExecutionsWidgetQuery) -> GetDailyExecutionsWidgetResponse:
        result = GetDailyExecutionsWidgetResponse()
        data_query = self.specifications.specify(query=query)
        result.Data = GetDailyExecutionsWidgetMapping.to_dto(data_query)
        return result
