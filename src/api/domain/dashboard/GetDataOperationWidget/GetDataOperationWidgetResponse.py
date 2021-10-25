from pdip.cqrs.decorators import responseclass
from domain.dashboard.GetDataOperationWidget.GetDataOperationWidgetDto import GetDataOperationWidgetDto


@responseclass
class GetDataOperationWidgetResponse:
	Data: GetDataOperationWidgetDto = None
