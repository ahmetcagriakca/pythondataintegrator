from typing import List
from infrastructure.cqrs.decorators.responseclass import responseclass
from domain.dashboard.GetDataOperationJobWidget.GetDataOperationJobWidgetDto import GetDataOperationJobWidgetDto


@responseclass
class GetDataOperationJobWidgetResponse:
	Data: List[GetDataOperationJobWidgetDto] = None
