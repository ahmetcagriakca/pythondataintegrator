from dataclasses import dataclass
from pdip.cqrs import IQuery

from src.application.dashboard.GetConnectionWidget.GetConnectionWidgetRequest import GetConnectionWidgetRequest
from src.application.dashboard.GetConnectionWidget.GetConnectionWidgetResponse import GetConnectionWidgetResponse


@dataclass
class GetConnectionWidgetQuery(IQuery[GetConnectionWidgetResponse]):
    request: GetConnectionWidgetRequest = None
