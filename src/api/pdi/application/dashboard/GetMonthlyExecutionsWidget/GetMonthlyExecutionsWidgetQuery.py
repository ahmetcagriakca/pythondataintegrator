from dataclasses import dataclass
from pdip.cqrs import IQuery

from pdi.application.dashboard.GetMonthlyExecutionsWidget.GetMonthlyExecutionsWidgetRequest import \
    GetMonthlyExecutionsWidgetRequest
from pdi.application.dashboard.GetMonthlyExecutionsWidget.GetMonthlyExecutionsWidgetResponse import \
    GetMonthlyExecutionsWidgetResponse


@dataclass
class GetMonthlyExecutionsWidgetQuery(IQuery[GetMonthlyExecutionsWidgetResponse]):
    request: GetMonthlyExecutionsWidgetRequest = None
