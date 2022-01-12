from dataclasses import dataclass
from pdip.cqrs import IQuery

from src.application.dashboard.GetMonthlyExecutionsWidget.GetMonthlyExecutionsWidgetRequest import \
    GetMonthlyExecutionsWidgetRequest
from src.application.dashboard.GetMonthlyExecutionsWidget.GetMonthlyExecutionsWidgetResponse import \
    GetMonthlyExecutionsWidgetResponse


@dataclass
class GetMonthlyExecutionsWidgetQuery(IQuery[GetMonthlyExecutionsWidgetResponse]):
    request: GetMonthlyExecutionsWidgetRequest = None
