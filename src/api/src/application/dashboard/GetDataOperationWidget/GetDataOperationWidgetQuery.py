from dataclasses import dataclass
from pdip.cqrs import IQuery

from src.application.dashboard.GetDataOperationWidget.GetDataOperationWidgetRequest import GetDataOperationWidgetRequest
from src.application.dashboard.GetDataOperationWidget.GetDataOperationWidgetResponse import \
    GetDataOperationWidgetResponse


@dataclass
class GetDataOperationWidgetQuery(IQuery[GetDataOperationWidgetResponse]):
    request: GetDataOperationWidgetRequest = None
