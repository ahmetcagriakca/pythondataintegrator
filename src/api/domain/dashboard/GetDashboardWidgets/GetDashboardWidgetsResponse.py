from typing import List
from infrastructure.cqrs.decorators.responseclass import responseclass


@responseclass
class GetDashboardWidgetsResponse:
    Data: List[any] = None

    def to_dict(self):
        return {"Data":[dict_data for dict_data in self.Data]}
