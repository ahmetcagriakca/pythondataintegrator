from dataclasses import dataclass
from pdip.cqrs import IQuery

from src.application.dashboard.GetExecutionStatusesWidget.GetExecutionStatusesWidgetRequest import \
    GetExecutionStatusesWidgetRequest
from src.application.dashboard.GetExecutionStatusesWidget.GetExecutionStatusesWidgetResponse import \
    GetExecutionStatusesWidgetResponse


@dataclass
class GetExecutionStatusesWidgetQuery(IQuery[GetExecutionStatusesWidgetResponse]):
    request: GetExecutionStatusesWidgetRequest = None
