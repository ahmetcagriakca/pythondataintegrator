from dataclasses import dataclass
from pdip.cqrs import IQuery

from pdi.application.dashboard.GetDataOperationJobExecutionWidget.GetDataOperationJobExecutionWidgetRequest import \
    GetDataOperationJobExecutionWidgetRequest
from pdi.application.dashboard.GetDataOperationJobExecutionWidget.GetDataOperationJobExecutionWidgetResponse import \
    GetDataOperationJobExecutionWidgetResponse


@dataclass
class GetDataOperationJobExecutionWidgetQuery(IQuery[GetDataOperationJobExecutionWidgetResponse]):
    request: GetDataOperationJobExecutionWidgetRequest = None
