from pdip.cqrs.decorators import responseclass

from src.application.dashboard.GetMonthlyExecutionsWidget.GetMonthlyExecutionsWidgetDto import \
    GetMonthlyExecutionsWidgetDto


@responseclass
class GetMonthlyExecutionsWidgetResponse:
    Data: GetMonthlyExecutionsWidgetDto = None
