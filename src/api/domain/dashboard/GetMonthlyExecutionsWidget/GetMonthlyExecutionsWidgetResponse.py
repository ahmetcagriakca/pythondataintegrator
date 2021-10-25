from pdip.cqrs.decorators import responseclass
from domain.dashboard.GetMonthlyExecutionsWidget.GetMonthlyExecutionsWidgetDto import GetMonthlyExecutionsWidgetDto


@responseclass
class GetMonthlyExecutionsWidgetResponse:
	Data: GetMonthlyExecutionsWidgetDto = None
