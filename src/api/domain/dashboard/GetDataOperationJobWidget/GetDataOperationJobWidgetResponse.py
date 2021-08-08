from typing import List
from domain.common.decorators.responseclass import responseclass
from domain.dashboard.GetDataOperationJobWidget.GetDataOperationJobWidgetDto import GetDataOperationJobWidgetDto


@responseclass
class GetDataOperationJobWidgetResponse:
	Data: List[GetDataOperationJobWidgetDto] = None
