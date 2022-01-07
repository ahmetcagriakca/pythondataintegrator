from pdip.cqrs.decorators import responseclass

from src.application.dashboard.GetConnectionWidget.GetConnectionWidgetDto import GetConnectionWidgetDto


@responseclass
class GetConnectionWidgetResponse:
    Data: GetConnectionWidgetDto = None
