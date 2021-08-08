from typing import List
from domain.common.decorators.responseclass import responseclass
from domain.dashboard.GetMonthlyExecutionsWidget.GetMonthlyExecutionsWidgetDto import GetMonthlyExecutionsWidgetDto


@responseclass
class GetMonthlyExecutionsWidgetResponse:
	Data: GetMonthlyExecutionsWidgetDto = None
