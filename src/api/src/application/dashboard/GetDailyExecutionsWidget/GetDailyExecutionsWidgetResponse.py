from typing import List

from pdip.cqrs.decorators import responseclass

from src.application.dashboard.GetDailyExecutionsWidget.GetDailyExecutionsWidgetDto import GetDailyExecutionsWidgetDto


@responseclass
class GetDailyExecutionsWidgetResponse:
    Data: List[GetDailyExecutionsWidgetDto] = None
