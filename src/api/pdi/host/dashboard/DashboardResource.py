from injector import inject
from pdip.api.base import ResourceBase
from pdip.cqrs import Dispatcher

from pdi.application.dashboard.GetDashboardWidgets.GetDashboardWidgetsQuery import GetDashboardWidgetsQuery
from pdi.application.dashboard.GetDashboardWidgets.GetDashboardWidgetsRequest import GetDashboardWidgetsRequest
from pdi.application.dashboard.GetDashboardWidgets.GetDashboardWidgetsResponse import GetDashboardWidgetsResponse


class DashboardResource(ResourceBase):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher

    def get(self, req: GetDashboardWidgetsRequest) -> GetDashboardWidgetsResponse:
        """
        Get All Connections
        """
        query = GetDashboardWidgetsQuery(request=req)
        res = self.dispatcher.dispatch(query)

        # import yaml
        # result = yaml.load(data)
        # return result["widgets"]
        return res
