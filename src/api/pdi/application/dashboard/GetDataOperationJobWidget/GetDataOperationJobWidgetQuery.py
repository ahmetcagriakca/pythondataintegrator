from dataclasses import dataclass
from pdip.cqrs import IQuery

from pdi.application.dashboard.GetDataOperationJobWidget.GetDataOperationJobWidgetRequest import \
    GetDataOperationJobWidgetRequest
from pdi.application.dashboard.GetDataOperationJobWidget.GetDataOperationJobWidgetResponse import \
    GetDataOperationJobWidgetResponse


@dataclass
class GetDataOperationJobWidgetQuery(IQuery[GetDataOperationJobWidgetResponse]):
    request: GetDataOperationJobWidgetRequest = None
