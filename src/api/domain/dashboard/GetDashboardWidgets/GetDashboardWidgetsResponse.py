from typing import List
from domain.common.decorators.responseclass import responseclass
from domain.dashboard.GetDashboardWidgets.GetDashboardWidgetsDto import GetDashboardWidgetsDto


@responseclass
class GetDashboardWidgetsResponse:
    Data: List[any] = None

    def to_dict(self):
        return {"Data":[dict_data for dict_data in self.Data]}
