from dataclasses import dataclass
from pdip.cqrs import IQuery
from domain.dashboard.GetDataOperationWidget.GetDataOperationWidgetRequest import GetDataOperationWidgetRequest
from domain.dashboard.GetDataOperationWidget.GetDataOperationWidgetResponse import GetDataOperationWidgetResponse


@dataclass
class GetDataOperationWidgetQuery(IQuery[GetDataOperationWidgetResponse]):
    request: GetDataOperationWidgetRequest = None
