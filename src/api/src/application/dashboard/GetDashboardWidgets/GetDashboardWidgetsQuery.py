from dataclasses import dataclass
from pdip.cqrs import IQuery

from src.application.dashboard.GetDashboardWidgets.GetDashboardWidgetsRequest import GetDashboardWidgetsRequest
from src.application.dashboard.GetDashboardWidgets.GetDashboardWidgetsResponse import GetDashboardWidgetsResponse


@dataclass
class GetDashboardWidgetsQuery(IQuery[GetDashboardWidgetsResponse]):
    request: GetDashboardWidgetsRequest = None
