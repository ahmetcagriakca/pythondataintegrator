from typing import List
from domain.common.decorators.responseclass import responseclass
from domain.dashboard.GetDataOperationWidget.GetDataOperationWidgetDto import GetDataOperationWidgetDto


@responseclass
class GetDataOperationWidgetResponse:
	Data: GetDataOperationWidgetDto = None
