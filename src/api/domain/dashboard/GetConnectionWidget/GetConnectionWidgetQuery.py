from dataclasses import dataclass
from pdip.cqrs import IQuery
from domain.dashboard.GetConnectionWidget.GetConnectionWidgetRequest import GetConnectionWidgetRequest
from domain.dashboard.GetConnectionWidget.GetConnectionWidgetResponse import GetConnectionWidgetResponse


@dataclass
class GetConnectionWidgetQuery(IQuery[GetConnectionWidgetResponse]):
    request: GetConnectionWidgetRequest = None
