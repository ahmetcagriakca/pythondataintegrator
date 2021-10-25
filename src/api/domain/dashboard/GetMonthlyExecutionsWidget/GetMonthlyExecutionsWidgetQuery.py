from dataclasses import dataclass
from pdip.cqrs import IQuery
from domain.dashboard.GetMonthlyExecutionsWidget.GetMonthlyExecutionsWidgetRequest import GetMonthlyExecutionsWidgetRequest
from domain.dashboard.GetMonthlyExecutionsWidget.GetMonthlyExecutionsWidgetResponse import GetMonthlyExecutionsWidgetResponse


@dataclass
class GetMonthlyExecutionsWidgetQuery(IQuery[GetMonthlyExecutionsWidgetResponse]):
    request: GetMonthlyExecutionsWidgetRequest = None
