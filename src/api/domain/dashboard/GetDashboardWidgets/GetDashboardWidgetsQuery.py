from dataclasses import dataclass
from pdip.cqrs import IQuery
from domain.dashboard.GetDashboardWidgets.GetDashboardWidgetsRequest import GetDashboardWidgetsRequest
from domain.dashboard.GetDashboardWidgets.GetDashboardWidgetsResponse import GetDashboardWidgetsResponse


@dataclass
class GetDashboardWidgetsQuery(IQuery[GetDashboardWidgetsResponse]):
    request: GetDashboardWidgetsRequest = None
