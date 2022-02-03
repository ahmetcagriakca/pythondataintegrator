from dataclasses import dataclass
from pdip.cqrs import IQuery

from src.application.dashboard.GetDailyExecutionsWidget.GetDailyExecutionsWidgetRequest import \
    GetDailyExecutionsWidgetRequest
from src.application.dashboard.GetDailyExecutionsWidget.GetDailyExecutionsWidgetResponse import \
    GetDailyExecutionsWidgetResponse


@dataclass
class GetDailyExecutionsWidgetQuery(IQuery[GetDailyExecutionsWidgetResponse]):
    request: GetDailyExecutionsWidgetRequest = None
