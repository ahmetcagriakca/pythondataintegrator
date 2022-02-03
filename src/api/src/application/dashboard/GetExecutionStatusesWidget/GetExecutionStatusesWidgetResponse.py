from typing import List

from pdip.cqrs.decorators import responseclass

from src.application.dashboard.GetExecutionStatusesWidget.GetExecutionStatusesWidgetDto import \
    GetExecutionStatusesWidgetDto


@responseclass
class GetExecutionStatusesWidgetResponse:
    Data: List[GetExecutionStatusesWidgetDto] = None
