from dataclasses import dataclass
from pdip.cqrs import IQuery

from src.application.dashboard.GetDataOperationJobExecutionWidget.GetDataOperationJobExecutionWidgetRequest import \
    GetDataOperationJobExecutionWidgetRequest
from src.application.dashboard.GetDataOperationJobExecutionWidget.GetDataOperationJobExecutionWidgetResponse import \
    GetDataOperationJobExecutionWidgetResponse


@dataclass
class GetDataOperationJobExecutionWidgetQuery(IQuery[GetDataOperationJobExecutionWidgetResponse]):
    request: GetDataOperationJobExecutionWidgetRequest = None
