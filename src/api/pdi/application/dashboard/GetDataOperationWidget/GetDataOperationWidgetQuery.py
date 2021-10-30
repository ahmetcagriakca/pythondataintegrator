from dataclasses import dataclass
from pdip.cqrs import IQuery

from pdi.application.dashboard.GetDataOperationWidget.GetDataOperationWidgetRequest import GetDataOperationWidgetRequest
from pdi.application.dashboard.GetDataOperationWidget.GetDataOperationWidgetResponse import \
    GetDataOperationWidgetResponse


@dataclass
class GetDataOperationWidgetQuery(IQuery[GetDataOperationWidgetResponse]):
    request: GetDataOperationWidgetRequest = None
