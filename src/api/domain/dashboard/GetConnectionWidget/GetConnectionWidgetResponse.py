from pdip.cqrs.decorators import responseclass
from domain.dashboard.GetConnectionWidget.GetConnectionWidgetDto import GetConnectionWidgetDto


@responseclass
class GetConnectionWidgetResponse:
	Data: GetConnectionWidgetDto = None
