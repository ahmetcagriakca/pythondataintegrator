import json

from injector import inject

from domain.dashboard.GetDashboardWidgets.GetDashboardWidgetsQuery import GetDashboardWidgetsQuery
from domain.dashboard.GetDashboardWidgets.GetDashboardWidgetsRequest import GetDashboardWidgetsRequest
from domain.dashboard.GetDashboardWidgets.GetDashboardWidgetsResponse import GetDashboardWidgetsResponse
from infrastructure.api.ResourceBase import ResourceBase
from infrastructure.api.decorators.Controller import controller
from infrastructure.cqrs.Dispatcher import Dispatcher



@controller()
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
