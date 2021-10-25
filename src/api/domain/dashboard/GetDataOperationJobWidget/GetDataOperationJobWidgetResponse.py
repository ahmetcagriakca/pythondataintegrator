from typing import List
from pdip.cqrs.decorators import responseclass
from domain.dashboard.GetDataOperationJobWidget.GetDataOperationJobWidgetDto import GetDataOperationJobWidgetDto


@responseclass
class GetDataOperationJobWidgetResponse:
	Data: List[GetDataOperationJobWidgetDto] = None
