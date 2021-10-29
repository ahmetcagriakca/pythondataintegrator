from dataclasses import dataclass
from pdip.cqrs import IQuery

from pdi.application.dashboard.GetDashboardWidgets.GetDashboardWidgetsRequest import GetDashboardWidgetsRequest
from pdi.application.dashboard.GetDashboardWidgets.GetDashboardWidgetsResponse import GetDashboardWidgetsResponse


@dataclass
class GetDashboardWidgetsQuery(IQuery[GetDashboardWidgetsResponse]):
    request: GetDashboardWidgetsRequest = None
