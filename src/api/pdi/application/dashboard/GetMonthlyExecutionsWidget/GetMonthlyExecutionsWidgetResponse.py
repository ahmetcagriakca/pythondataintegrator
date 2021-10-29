from pdip.cqrs.decorators import responseclass

from pdi.application.dashboard.GetMonthlyExecutionsWidget.GetMonthlyExecutionsWidgetDto import \
    GetMonthlyExecutionsWidgetDto


@responseclass
class GetMonthlyExecutionsWidgetResponse:
    Data: GetMonthlyExecutionsWidgetDto = None
